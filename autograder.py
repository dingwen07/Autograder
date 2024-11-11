import json
import sys
import os
import argparse
import copy
import shutil

import tasks
import criteria

bindings = {}
bindings['interpreter'] = sys.executable
error_log = ''

def run_tasks(task_list):
    global error_log
    for task in task_list:
        if task['evalparams']:
            parameters = map(eval, task['parameters'])
        else:
            parameters = task['parameters']
        
        task_id = 'tasks.' + task['task']
        try:
            ret = eval(task_id)(*parameters)
            if 'bindret' in task:
                bindings[task['bindret']] = ret
            if 'setenv' in task:
                os.environ[task['setenv']] = str(ret)
            if ret == 504:
                error_log += f'Task {task["task"]} execution timed out ({task})\n'
        except Exception as e:
            error_log += f'Task {task["task"]} execution failed with error: {e}\n'


if __name__ == '__main__':
    tasks.bindings = bindings
    criteria.bindings = bindings

    parser = argparse.ArgumentParser(description='Autograder')
    parser.add_argument('specification', nargs='?', default='specification.json', help='Specification file')
    parser.add_argument('-b', '--binding', action='append', help='Binding to be passed to specification')
    args = parser.parse_args()

    specification = json.load(open(args.specification, 'r'))

    if args.binding:
        for binding in args.binding:
            if '=' in binding:
                key, value = binding.split('=', 1)
                bindings[key] = value
            else:
                print(f'Invalid binding: {binding}')
    
    error_log = ''
    run_tasks(specification['tasks'])

    points_obtained = 0
    points_total = 0
    test_passed = 0
    autograder_report = specification['name'] + '\n'
    autograder_report += 'Autograder Report\n\n'
    autograder_report += 'Local Bindings:\n'
    for key, value in bindings.items():
        autograder_report += f'\t{key} = {repr(value)}\n'
    autograder_report += '\n'
    if error_log != '':
        autograder_report += 'Task Execution Error Log:\n'
        autograder_report += error_log + '\n\n'
        error_log = ''


    test_id = 0
    # Legacy config compatibility
    if 'criteria' not in specification:
        specification['criteria'] = specification['criterias']
        print('WARNING: Legacy config in specification file: criterias', file=sys.stderr)

    for criterion in specification['criteria']:
        test_id += 1
        points_total += criterion['points']
        autograder_report += f'Test {test_id}: {criterion["name"]}\n'
        autograder_report += f'Points:\t\t{criterion["points"]}{f' (Deduct {criterion['deduct']} pts if Failed)' if 'deduct' in criterion else ''}\n'

        if criterion['expected']['evalvalue']:
            try:
                criterion['expected']['value'] = eval(criterion['expected']['value'])
            except Exception as e:
                # print(f'criterion {criterion["criterion"]} expected value eval failed with error: {e}')
                autograder_report += f'criterion {criterion["criterion"]} expected value eval failed with error: {e}\n'
                criterion['expected']['value'] = False
        
        if criterion['evalparams']:
            parameters = map(eval, criterion['parameters'])
        else:
            parameters = criterion['parameters']
        parameters_copy = copy.deepcopy(parameters)

        # Legacy config compatibility
        if 'criterion' not in criterion:
            criterion['criterion'] = criterion['criteria']
            print('WARNING: Legacy config in specification file: criteria.criteria', file=sys.stderr)
        criterion_id = 'criteria.' + criterion['criterion']
        try:
            ret = eval(criterion_id)(*parameters)
        except Exception as e:
            # print(f'criterion {criterion["criterion"]} evaluation failed with error: {e}')
            autograder_report += f'criterion {criterion["criterion"]} evaluation failed with error: {e}\n'
            ret = None

        if criterion['public']:
            autograder_report += f'Description:\t{criterion["description"]}\n'
            parameters_str = ', '.join(map(repr, parameters_copy))
            autograder_report += f'Criterion:\t{criterion["criterion"]}({parameters_str})\n'
            autograder_report += f'Expected:\t{'' if criterion['expected']['eq'] else 'Not '}{repr(criterion["expected"]["value"])}\n'
            autograder_report += f'Actual:\t\t{repr(ret)}\n'
        else:
            autograder_report += f'Description:\tPrivate Test\n'

        if (ret == criterion['expected']['value']) == (criterion['expected']['eq']):
            points_obtained += criterion['points']
            autograder_report += f'Result:\t\tPassed\n'
            test_passed += 1
        else:
            autograder_report += f'Result:\t\tFailed\n'
            if 'deduct' in criterion:
                points_obtained -= criterion['deduct']
                autograder_report += f'Deducted: {criterion["deduct"]} pts\n'
        autograder_report += '\n'

    autograder_report += f'Tests Passed:\t{test_passed}/{test_id}\n'
    autograder_report += f'Points Earned:\t{points_obtained}/{points_total}\n'
    print(autograder_report)

    if 'report' in specification:
        with open(specification['report'], 'w') as file:
            file.write(autograder_report)
    
    # retrieve files if running in docker
    if 'LIMBO' in os.environ:
        for file in specification['retrieve']:
            shutil.copy(file, os.environ['LIMBO'])
            print(f'Retrieved {file}', file=sys.stderr)

    # cleanup
    r = input('Press Enter to Cleanup and Exit...')
    r = r.strip()
    if r != '' and shutil.which(r):
        os.system(r)
    run_tasks(specification['cleanup'])

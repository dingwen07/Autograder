import json
import sys
import os
import argparse

import tasks
import criterias

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
                os.environ[task['addenv']] = str(ret)
            if ret == 504:
                error_log += f'Task {task["task"]} execution timed out ({task})\n'
        except Exception as e:
            error_log += f'Task {task["task"]} execution failed with error: {e}\n'


if __name__ == '__main__':
    criterias.bindings = bindings

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
    if error_log != '':
        autograder_report += 'Task Execution Error Log:\n'
        autograder_report += error_log + '\n\n'
        error_log = ''


    test_id = 0
    for criteria in specification['criterias']:
        test_id += 1
        points_total += criteria['points']
        autograder_report += f'Test {test_id}: {criteria["name"]}\n'
        autograder_report += f'Points:\t\t{criteria["points"]}{f' (Deduct {criteria['deduct']}pts if Failed)' if 'deduct' in criteria else ''}\n'

        if criteria['expected']['evalvalue']:
            try:
                criteria['expected']['value'] = eval(criteria['expected']['value'])
            except Exception as e:
                # print(f'Criteria {criteria["criteria"]} expected value eval failed with error: {e}')
                autograder_report += f'Criteria {criteria["criteria"]} expected value eval failed with error: {e}\n'
                criteria['expected']['value'] = False
        
        if criteria['evalparams']:
            parameters = map(eval, criteria['parameters'])
        else:
            parameters = criteria['parameters']

        criteria_id = 'criterias.' + criteria['criteria']
        try:
            ret = eval(criteria_id)(*parameters)
        except Exception as e:
            # print(f'Criteria {criteria["criteria"]} evaluation failed with error: {e}')
            autograder_report += f'Criteria {criteria["criteria"]} evaluation failed with error: {e}\n'
            ret = None

        if criteria['public']:
            autograder_report += f'Description:\t{criteria["description"]}\n'
            autograder_report += f'Criteria:\t{criteria["criteria"]}\n'
            autograder_report += f'Expected:\t{'' if criteria['expected']['eq'] else 'Not '}{criteria["expected"]["value"]}\n'
            autograder_report += f'Actual:\t\t{ret}\n'
        else:
            autograder_report += f'Description:\tPrivate Test\n'

        if (ret == criteria['expected']['value']) == (criteria['expected']['eq']):
            points_obtained += criteria['points']
            autograder_report += f'Result:\t\tPassed\n'
            test_passed += 1
        else:
            autograder_report += f'Result:\t\tFailed\n'
            if 'deduct' in criteria:
                points_obtained -= criteria['deduct']
                autograder_report += f'Deducted: {criteria["deduct"]}pts\n'
        autograder_report += '\n'

    print(autograder_report)
    print(f'Tests Passed:\t{test_passed}/{test_id}')
    print(f'Points Earned:\t{points_obtained}/{points_total}')

    # cleanup
    input('Press Enter to Cleanup and Exit...')
    run_tasks(specification['cleanup'])

import json
import sys

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
            if ret == 504:
                error_log += f'Task {task["task"]} execution timed out ({task})\n'
        except Exception as e:
            error_log += f'Task {task["task"]} execution failed with error: {e}\n'


if __name__ == '__main__':
    criterias.bindings = bindings
    specification = json.load(open('specification.json'))

    error_log = ''
    run_tasks(specification['tasks'])

    points_obtained = 0
    points_total = 0
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
        autograder_report += f'Points: {criteria["points"]}{f' (Deduct {criteria['deduct']}pts if Failed)' if 'deduct' in criteria else ''}\n'

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
            autograder_report += f'Description: {criteria["description"]}\n'
            autograder_report += f'Expected: {'' if criteria['expected']['eq'] else 'Not '}{criteria["expected"]["value"]}\n'
            autograder_report += f'Actual: {ret}\n'
        else:
            autograder_report += f'Description: Private Test\n'

        if (ret == criteria['expected']['value']) == (criteria['expected']['eq']):
            points_obtained += criteria['points']
            autograder_report += f'Result: Passed\n'
        else:
            autograder_report += f'Result: Failed\n'
            if 'deduct' in criteria:
                points_obtained -= criteria['deduct']
                autograder_report += f'Deducted: {criteria["deduct"]}pts\n'
        autograder_report += '\n'

    print(autograder_report)
    print(f'Points obtained: {points_obtained}/{points_total}')

    # cleanup
    input('Press Enter to Cleanup and Exit...')
    run_tasks(specification['cleanup'])

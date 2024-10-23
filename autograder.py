import json
import sys

import tasks
import criterias

bindings = {}
bindings['interpreter'] = sys.executable

def run_tasks(task_list):
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
        except Exception as e:
            print(f'Task {task["task"]} failed with error: {e}')


if __name__ == '__main__':
    criterias.bindings = bindings
    specification = json.load(open('specification.json'))

    run_tasks(specification['tasks'])

    points_obtained = 0
    points_total = 0
    points_report = specification['name'] + '\n'
    points_report += 'Autograder Report\n\n'
    test_id = 0

    for criteria in specification['criterias']:
        test_id += 1
        points_total += criteria['points']
        if criteria['evalparams']:
            parameters = map(eval, criteria['parameters'])
        else:
            parameters = criteria['parameters']

        criteria_id = 'criterias.' + criteria['criteria']

        try:
            ret = eval(criteria_id)(*parameters)
        except Exception as e:
            print(f'Criteria {criteria["criteria"]} evaluation failed with error: {e}')
            ret = None

        points_report += f'Test {test_id}: {criteria["name"]}\n'
        points_report += f'Points: {criteria["points"]}{f' (Deduct {criteria['deduct']}pts if Failed)' if 'deduct' in criteria else ''}\n'

        if criteria['expected']['evalvalue']:
            try:
                criteria['expected']['value'] = eval(criteria['expected']['value'])
            except Exception as e:
                print(f'Criteria {criteria["criteria"]} expected evalvalue failed with error: {e}')
                criteria['expected']['value'] = False

        if criteria['public']:
            points_report += f'Description: {criteria["description"]}\n'
            points_report += f'Expected: {'' if criteria['expected']['eq'] else 'Not '}{criteria["expected"]["value"]}\n'
            points_report += f'Actual: {ret}\n'
        else:
            points_report += f'Description: Private Test\n'

        if (ret == criteria['expected']['value']) == (criteria['expected']['eq']):
            points_obtained += criteria['points']
            points_report += f'Result: Passed\n'
        else:
            points_report += f'Result: Failed\n'
            if 'deduct' in criteria:
                points_obtained -= criteria['deduct']
                points_report += f'Deducted: {criteria["deduct"]}pts\n'
        points_report += '\n'

    print(points_report)
    print(f'Points obtained: {points_obtained}/{points_total}')

    # cleanup
    input('Press Enter to Cleanup and Exit...')
    run_tasks(specification['cleanup'])

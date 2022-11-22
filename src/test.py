from main import ExperimentTracker

tracker = ExperimentTracker(['notes', 'rmse'], 'test.jsonl', 'rmse', file_format='json')
tracker.add_experiment({'notes':'nothing', 'rmse':2})
tracker.add_experiment({'notes':'nothing', 'rmse':1})
print(tracker.__str__())
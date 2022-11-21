import jsonlines
import pandas as pd

class ExperimentTracker():
    """A lightweight experiment tracker that saves json output to a file
    """
    def __init__(self, e_args, file_name, sort_column, use_custom_columns=False, custom_columns=None, file_format='json'):
        """
        Args: 
            e_args: columns required to be provided for each new experiment
            file_name: file for outputs to be saved to
            sort_column: columns for pandas dataframe to be saved to
            custom_columns: custom column names like e_args
        """
        supported_file_formats = ['json', 'csv']

        self.experiments = {key:[] for key in e_args}
        self.args = e_args
        self.file_name = file_name
        self.experiments_df = pd.DataFrame(self.experiments)
        self.sort_column = sort_column
        self.use_custom_columns = use_custom_columns
        if use_custom_columns:
            self.custom_columns = custom_columns
        if file_format not in supported_file_formats:
            raise Exception("Specified format to save experiments " + file_format + " not supported. \n" + "You may save files in the following formats: " + ' '.join(supported_file_formats))
        self.file_format = file_format
        if self.file_format == 'json':
            with jsonlines.open(file_name, 'a') as file:
                file.write(self.experiments)

    def verify_info(self, info):
        """Verifies if the provided new experiemnt matches the columns provided in __init__

        Args:
            info: the new experiment to be saved

        Raises: 
            Exception: If the info keys do not match self.args
        """
        for i in info:
            if i not in self.args:
                raise Exception("Arg dictionary key: " + i + " not in provided required experiment information")

    def add_experiment(self, info, custom_column_values=None):
        """Adds a new experiment

        Args:
            info: the new experiment to be added
            custom_column_values: like info except for custom columns

        Returns:
            The experiments dataframe
        """
        self.verify_info(info)
        for key in self.experiments.keys():
            self.experiments[key].append(info[key])      
        self.experiments_df = pd.DataFrame(self.experiments).sort_values(by=[self.sort_column])
        if self.use_custom_columns:
            for i, j in enumerate(self.custom_columns):
                self.experiments_df[j] = custom_column_values[i]
        return self.experiments_df

    def load_experiments_df(self):
        """Provides the latest version of the experiments dataframe

        Returns:
            The experiments dataframe
        """
        return self.experiments_df
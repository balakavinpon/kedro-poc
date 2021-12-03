# Copyright 2021 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited ("QuantumBlack") name and logo
# (either separately or in combination, "QuantumBlack Trademarks") are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
# or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.
"""
This is a boilerplate pipeline 'model_training'
generated using Kedro 0.17.4
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def data_acquisition(params, data):
    #data = pd.read_csv(r"data/01_raw/diabetes.csv")
    raw_data = data
    print(data.loc[[1]])
    return raw_data 

def feature_engineering(params, raw_data):
    df = raw_data
    df1 = df.dropna()
    cleaned_data = df1
    return cleaned_data

def train_test_split_fun(params, cleaned_data):
    value = params['ratio']
    training_data = cleaned_data.drop('Outcome',axis=1)
    testing_data = cleaned_data['Outcome']
    X_train, X_test, y_train, y_test = train_test_split(training_data, testing_data, test_size = value, random_state=42)
    return X_train, X_test, y_train, y_test

def model_training(params, X_train, y_train):
    rc = RandomForestClassifier(max_depth=2, random_state=0)
    model = rc.fit(X_train, y_train)
    return model

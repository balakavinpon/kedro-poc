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

from kedro.pipeline import Pipeline, node
from functools import update_wrapper, partial
from pkg.pipelines.model_training.nodes import (
    data_acquisition,
    feature_engineering,
    train_test_split_fun,
    model_training)

def create_pipeline(**kwargs):
    model_training_pipeline = Pipeline([node(data_acquisition,
                                  inputs='parameters',
                                  outputs='dataset'),
                     node(feature_engineering,
                                 inputs=['parameters','dataset'],
                                 outputs='cleaned_dataset'),
                    node(train_test_split_fun,
                                 inputs=['parameters','cleaned_dataset'],
                                 outputs=['x_train','x_test','y_train','y_test']),
                     node(model_training,
                                 inputs=['parameters','x_train', 'y_train'],
                                 outputs='model'),
                                    ])
    return model_training_pipeline

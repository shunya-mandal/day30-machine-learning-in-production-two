import os
import json
import pandas as pd
import pickle
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def apicall():
	"""API Call
	
	Pandas dataframe (sent as a payload) from API Call
	"""
	try:
		test_json = request.get_json()
		test = pd.read_json(test_json, orient='split')
	except Exception as e:
		raise e
	
	if test.empty:
		return(bad_request())
	else:
		clf = 'model1.pk'

		#Load the saved model
		loaded_model = pickle.load(open(os.getcwd()+'/models/'+str(clf), 'rb'))
		predictions = loaded_model.predict(test)
		
		"""Add the predictions as Series to a new pandas dataframe
								OR
		   Depending on the use-case, the entire test data appended with the new files
		"""
		prediction_series = pd.Series(predictions)
		
		"""We can be as creative in sending the responses.
		   But we need to send the response codes as well.
		"""
		responses = jsonify(predictions=prediction_series.to_json())
		responses.status_code = 200

		return (responses)


@app.errorhandler(400)
def bad_request(error=None):
	message = {
			'status': 400,
			'message': 'Bad Request: ' + request.url + '--> Please check your data payload...',
	}
	resp = jsonify(message)
	resp.status_code = 400

	return resp


if __name__ == '__main__':
	app.run(debug=False, host="0.0.0.0", port=5000)

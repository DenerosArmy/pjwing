import OpenTokSDK

api_key = "14260652"
api_secret = "4611823556deeea92d01eea637831386e4d50d3d"
session_address = "https://api.opentok.com/hl"

def create_session():
	opentok_sdk = OpenTokSDK.OpenTokSDK(api_key, api_secret)
	session_properties = {OpenTokSDK.SessionProperties.p2p_preference: "enabled"}
	session = opentok_sdk.create_session(session_address, session_properties)
	session_id = session.session_id
	return session_id

def generate_token(session_id):
	opentok_sdk = OpenTokSDK.OpenTokSDK(api_key, api_secret)
	session = opentok_sdk.create_session(session_address)
	token = opentok_sdk.generate_token(session.session_id) 
	return token

	

	





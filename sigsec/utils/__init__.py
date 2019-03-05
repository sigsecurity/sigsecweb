from flask import jsonify

def success(status, data=None, reason=None):
  status = bool(status)
  message = {"success" : status}

  if data and isinstance(data, dict):
    message = {**message, **data}
  
  if reason and isinstance(reason, str):
    message["reason"] = reason
  
  return jsonify(message)


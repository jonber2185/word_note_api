import traceback
from .base import AppError
from flask import jsonify, request

def register_error_handlers(app):
    
    @app.errorhandler(404)
    def handle_404_error(e):
        return jsonify({
            "error": "NotFound",
            "message": "URL not found"
        }), 404

    @app.errorhandler(405)
    def handle_405_error(e):
        return jsonify({
            "error": "MethodNotAllowed",
            "message": f"The method {request.method} is not allowed for this endpoint."
        }), 405

    @app.errorhandler(AppError)
    def handle_app_error(e):
        response_body = {
            "error": type(e).__name__,
            "message": str(e.message),
        }
        if e.payload: response_body["payload"] = e.payload
            
        return jsonify(response_body), e.status_code

    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        print(f"\n[Unexpected Error]: {e}")
        traceback.print_exc() 
        
        return jsonify({
            "error": "InternalServerError",
            "message": "An unexpected error occurred on the server."
        }), 500
    
from flask import Flask,request
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from operations_service import OperationsService
from operations_controller import OperationsController


def configure_app_logging(base_dir: Path):
    """Configure application-wide logging"""
    logs_dir = base_dir / "operations" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    # Application logger
    app_logger = logging.getLogger('operations_app')
    app_logger.setLevel(logging.INFO)
    
    # File handler
    file_handler = RotatingFileHandler(
        logs_dir / 'operations_app.log',
        maxBytes=1024*1024,
        backupCount=5
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    app_logger.addHandler(file_handler)
    
    # Console handler for development
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    ))
    app_logger.addHandler(console_handler)
    
    return app_logger

app = Flask(__name__)

# Initialize services and logging
base_dir = Path(__file__).parent.parent  # src/platform
app_logger = configure_app_logging(base_dir)
service = OperationsService(base_dir)
controller = OperationsController(service)

# Register routes
app.add_url_rule(
    '/api/operations/operation',
    view_func=controller.create_operation,
    methods=['POST']
)


app.add_url_rule(
    '/api/operations',
    view_func=controller.list_operations,
    methods=['GET']
)

app.add_url_rule(
    '/api/agents',
    view_func=controller.get_agents,
    methods=['GET']
)


app.add_url_rule(
    '/api/operations/start/<operation_name>',  # Path parameter
    view_func=controller.start_operation,
    methods=['POST']  # Only POST allowed
)

app.add_url_rule(
    '/api/investigations',
    view_func=controller.list_investigations,
    methods=['GET']
)

app.add_url_rule(
    '/api/investigations/trigger/<investigation_name>',
    view_func=controller.trigger_investigation,
    methods=['POST']
)


@app.before_request
def log_request_start():
    """Log incoming requests"""
    app_logger.info(f"Request started: {request.method} {request.path}")

@app.after_request
def log_request_completion(response):
    """Log completed requests"""
    app_logger.info(
        f"Request completed: {request.method} {request.path} "
        f"=> {response.status_code}"
    )
    return response



if __name__ == '__main__':
    app_logger.info("Starting Operations API Service")
    app.run(host='0.0.0.0', port=5000, debug=True)
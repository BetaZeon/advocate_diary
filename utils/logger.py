"""
Logging utility for Advocate Diary application
"""
import logging
import os
import streamlit as st
from datetime import datetime
from pathlib import Path

class AdvocateDiaryLogger:
    """Centralized logging for Advocate Diary application"""
    
    def __init__(self, log_file="advocate_diary.log"):
        self.log_file = log_file
        self.logger = None
        self.is_production = self._detect_production_environment()
        self.in_memory_logs = []  # For production logging
        self.max_memory_logs = 1000  # Keep last 1000 log entries in memory
        self.sheets_logger = None  # Google Sheets logger for production
        self._setup_logger()
        self._setup_sheets_logging()
    
    def _detect_production_environment(self):
        """Detect if running in production (Streamlit Cloud)"""
        # Check for Streamlit Cloud environment variables
        if os.getenv('STREAMLIT_SHARING_MODE') == 'true':
            return True
        if os.getenv('STREAMLIT_SERVER_PORT') and os.getenv('STREAMLIT_SERVER_ADDRESS'):
            return True
        # Check if running in a containerized environment
        if os.path.exists('/.dockerenv'):
            return True
        return False
    
    def _setup_logger(self):
        """Setup the logger with file and console handlers"""
        # Create logger
        self.logger = logging.getLogger("advocate_diary")
        self.logger.setLevel(logging.DEBUG)
        
        # Clear any existing handlers
        self.logger.handlers.clear()
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        simple_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        
        if self.is_production:
            # Production: Only console logging + in-memory storage
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(simple_formatter)
            self.logger.addHandler(console_handler)
            
            # Log initial setup
            self.logger.info("=" * 60)
            self.logger.info("Advocate Diary Application Started (PRODUCTION)")
            self.logger.info("Logging to console and in-memory storage")
            self.logger.info("=" * 60)
        else:
            # Development: File + console logging
            # Create logs directory if it doesn't exist
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            
            # Full path to log file
            log_path = log_dir / self.log_file
            
            # File handler (detailed logs)
            file_handler = logging.FileHandler(log_path, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(detailed_formatter)
            
            # Console handler (simple logs for development)
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(simple_formatter)
            
            # Add handlers to logger
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
            
            # Log initial setup
            self.logger.info("=" * 60)
            self.logger.info("Advocate Diary Application Started (DEVELOPMENT)")
            self.logger.info(f"Log file: {log_path.absolute()}")
            self.logger.info("=" * 60)
    
    def _setup_sheets_logging(self):
        """Setup Google Sheets logging for production"""
        if self.is_production:
            try:
                from utils.sheets_logger import sheets_logger
                self.sheets_logger = sheets_logger
                if self.sheets_logger.is_available:
                    self.logger.info("Google Sheets logging enabled for production")
                else:
                    self.logger.warning("Google Sheets logging not available, using in-memory only")
            except Exception as e:
                self.logger.error(f"Failed to setup Google Sheets logging: {e}")
                self.sheets_logger = None
    
    def _add_to_memory_log(self, level, message, **kwargs):
        """Add log entry to in-memory storage for production"""
        if self.is_production:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_entry = f"{timestamp} - {level.upper()} - {message}"
            self.in_memory_logs.append(log_entry)
            
            # Keep only the last max_memory_logs entries
            if len(self.in_memory_logs) > self.max_memory_logs:
                self.in_memory_logs = self.in_memory_logs[-self.max_memory_logs:]
            
            # Also write to Google Sheets if available
            if self.sheets_logger and self.sheets_logger.is_available:
                function_name = kwargs.get('function_name', '')
                context = kwargs.get('context', '')
                error_details = kwargs.get('error_details', '')
                self.sheets_logger.log(level, message, function_name, context, error_details)
    
    def debug(self, message, **kwargs):
        """Log debug message"""
        # Extract custom parameters before passing to logger
        custom_params = {k: v for k, v in kwargs.items() if k in ['function_name', 'context', 'error_details']}
        logger_kwargs = {k: v for k, v in kwargs.items() if k not in ['function_name', 'context', 'error_details']}
        
        self.logger.debug(message, **logger_kwargs)
        self._add_to_memory_log('debug', message, **custom_params)
    
    def info(self, message, **kwargs):
        """Log info message"""
        # Extract custom parameters before passing to logger
        custom_params = {k: v for k, v in kwargs.items() if k in ['function_name', 'context', 'error_details']}
        logger_kwargs = {k: v for k, v in kwargs.items() if k not in ['function_name', 'context', 'error_details']}
        
        self.logger.info(message, **logger_kwargs)
        self._add_to_memory_log('info', message, **custom_params)
    
    def warning(self, message, **kwargs):
        """Log warning message"""
        # Extract custom parameters before passing to logger
        custom_params = {k: v for k, v in kwargs.items() if k in ['function_name', 'context', 'error_details']}
        logger_kwargs = {k: v for k, v in kwargs.items() if k not in ['function_name', 'context', 'error_details']}
        
        self.logger.warning(message, **logger_kwargs)
        self._add_to_memory_log('warning', message, **custom_params)
    
    def error(self, message, **kwargs):
        """Log error message"""
        # Extract custom parameters before passing to logger
        custom_params = {k: v for k, v in kwargs.items() if k in ['function_name', 'context', 'error_details']}
        logger_kwargs = {k: v for k, v in kwargs.items() if k not in ['function_name', 'context', 'error_details']}
        
        self.logger.error(message, **logger_kwargs)
        self._add_to_memory_log('error', message, **custom_params)
    
    def critical(self, message, **kwargs):
        """Log critical message"""
        # Extract custom parameters before passing to logger
        custom_params = {k: v for k, v in kwargs.items() if k in ['function_name', 'context', 'error_details']}
        logger_kwargs = {k: v for k, v in kwargs.items() if k not in ['function_name', 'context', 'error_details']}
        
        self.logger.critical(message, **logger_kwargs)
        self._add_to_memory_log('critical', message, **custom_params)
    
    def log_function_call(self, func_name, args=None, kwargs=None):
        """Log function call with parameters"""
        args_str = f"args={args}" if args else ""
        kwargs_str = f"kwargs={kwargs}" if kwargs else ""
        params = ", ".join(filter(None, [args_str, kwargs_str]))
        context = f"Function call: {func_name}({params})"
        self.debug(f"Calling {func_name}({params})", function_name=func_name, context=context)
    
    def log_function_result(self, func_name, result=None, success=True):
        """Log function result"""
        status = "SUCCESS" if success else "FAILED"
        result_str = f" -> {result}" if result is not None else ""
        context = f"Function result: {func_name} {status}"
        self.debug(f"{func_name} {status}{result_str}", function_name=func_name, context=context)
    
    def log_google_sheets_operation(self, operation, details=None):
        """Log Google Sheets specific operations"""
        details_str = f" - {details}" if details else ""
        context = f"Google Sheets operation: {operation}"
        self.info(f"Google Sheets {operation}{details_str}", function_name="google_sheets", context=context)
    
    def log_case_operation(self, operation, case_number=None, location=None):
        """Log case-specific operations"""
        case_info = f" (Case: {case_number}, Location: {location})" if case_number else ""
        context = f"Case operation: {operation}"
        if case_number:
            context += f", Case Number: {case_number}"
        if location:
            context += f", Location: {location}"
        self.info(f"Case {operation}{case_info}", function_name="case_operation", context=context)
    
    def log_error_with_context(self, error, context=None):
        """Log error with additional context"""
        context_str = f" | Context: {context}" if context else ""
        error_details = str(error)
        self.error(f"Error: {str(error)}{context_str}", exc_info=True, context=context, error_details=error_details)
    
    def get_memory_logs(self, limit=None):
        """Get in-memory logs for production viewing"""
        if not self.is_production:
            return []
        
        logs = self.in_memory_logs
        if limit:
            logs = logs[-limit:]
        return logs
    
    def get_logs_as_text(self, limit=None):
        """Get logs as formatted text"""
        if self.is_production:
            # Try Google Sheets first, fallback to memory
            if self.sheets_logger and self.sheets_logger.is_available:
                try:
                    sheets_logs = self.sheets_logger.get_recent_logs(limit or 100)
                    if sheets_logs:
                        formatted_logs = []
                        for log in sheets_logs:
                            timestamp = log.get('Timestamp', '')
                            level = log.get('Level', '')
                            message = log.get('Message', '')
                            function_name = log.get('Function', '')
                            context = log.get('Context', '')
                            
                            log_line = f"{timestamp} - {level} - {message}"
                            if function_name:
                                log_line += f" [{function_name}]"
                            if context:
                                log_line += f" | {context}"
                            formatted_logs.append(log_line)
                        
                        return '\n'.join(formatted_logs)
                except Exception as e:
                    self.logger.error(f"Failed to get logs from Google Sheets: {e}")
            
            # Fallback to memory logs
            logs = self.get_memory_logs(limit)
            return '\n'.join(logs)
        else:
            # In development, try to read from file
            log_file = Path("logs") / self.log_file
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if limit:
                        lines = content.strip().split('\n')
                        return '\n'.join(lines[-limit:])
                    return content
            return "No log file found"
    
    def clear_memory_logs(self):
        """Clear in-memory logs"""
        self.in_memory_logs = []
    
    def clear_all_logs(self):
        """Clear all logs (memory and Google Sheets)"""
        self.clear_memory_logs()
        if self.sheets_logger and self.sheets_logger.is_available:
            self.sheets_logger.clear_logs()
    
    def get_sheets_logs(self, limit=None):
        """Get logs from Google Sheets"""
        if self.sheets_logger and self.sheets_logger.is_available:
            return self.sheets_logger.get_recent_logs(limit)
        return []

# Global logger instance
logger = AdvocateDiaryLogger()

# Convenience functions for easy access
def debug(message, **kwargs):
    logger.debug(message, **kwargs)

def info(message, **kwargs):
    logger.info(message, **kwargs)

def warning(message, **kwargs):
    logger.warning(message, **kwargs)

def error(message, **kwargs):
    logger.error(message, **kwargs)

def critical(message, **kwargs):
    logger.critical(message, **kwargs)

def log_function_call(func_name, args=None, kwargs=None):
    logger.log_function_call(func_name, args, kwargs)

def log_function_result(func_name, result=None, success=True):
    logger.log_function_result(func_name, result, success)

def log_google_sheets_operation(operation, details=None):
    logger.log_google_sheets_operation(operation, details)

def log_case_operation(operation, case_number=None, location=None):
    logger.log_case_operation(operation, case_number, location)

def log_error_with_context(error, context=None):
    logger.log_error_with_context(error, context)

def get_memory_logs(limit=None):
    return logger.get_memory_logs(limit)

def get_logs_as_text(limit=None):
    return logger.get_logs_as_text(limit)

def clear_memory_logs():
    logger.clear_memory_logs()

def clear_all_logs():
    logger.clear_all_logs()

def get_sheets_logs(limit=None):
    return logger.get_sheets_logs(limit)

def is_production():
    return logger.is_production

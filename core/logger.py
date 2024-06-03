import structlog

def _add_severity(_, method: str, event_dict: dict) -> dict:
    event_dict["severity"] = method.upper()

    if method in ("error", "exception"):
        event_dict["@type"] = "type.googleapis.com/google.devtools.clouderrorreporting.v1beta1.ReportedErrorEvent"

    return event_dict

def _format_event_dict(_, __, event_dict: dict) -> dict:

    event_dict["reportLocation"] = {}
    event_dict["reportLocation"]["filePath"] = event_dict.pop("filename")
    event_dict["reportLocation"]["lineNumber"] = event_dict.pop("lineno")
    event_dict["reportLocation"]["functionName"] = event_dict.pop("func_name")

    return event_dict


def init_logger_config() -> structlog.stdlib.BoundLogger:

    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.EventRenamer("message"),
        structlog.processors.format_exc_info,
        structlog.processors.CallsiteParameterAdder(
            [
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.LINENO,
            ]
        ),
        _add_severity, # user-made
        _format_event_dict, # user-made
        structlog.processors.JSONRenderer(),
    ]


    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
    )

    return structlog.stdlib.get_logger()

logger = init_logger_config()
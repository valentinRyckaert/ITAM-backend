from ..dependencies import SessionDep, get_current_user
import logging

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - Method: %(method)s - URL: %(url)s - Status: %(status)s - User: %(user)s - Message: [%(message)s]'
)

logger = logging.getLogger('ITAM')
logger.setLevel(logging.WARNING)
fh = logging.FileHandler('api.log', 'a')
fh.setFormatter(formatter)
logger.addHandler(fh)
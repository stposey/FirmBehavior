from os import environ
SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1, participation_fee=0)
SESSION_CONFIGS = [dict(name='Benchmark', num_demo_participants=None, app_sequence=['FirmBehaviorBenchmark']), dict(name='Signal', num_demo_participants=None, app_sequence=['FirmBehaviorSignal']), dict(name='Search', num_demo_participants=None, app_sequence=['FirmBehaviorSearch']), dict(name='SearchSignal', num_demo_participants=None, app_sequence=['FirmBehaviorSearchSignal']), dict(name='SignalTest', num_demo_participants=None, app_sequence=['FirmBehaviorSignal'], use_browser_bots=True), dict(name='TestSearch', num_demo_participants=None, app_sequence=['FirmBehaviorSearch'], use_browser_bots=True), dict(name='BenchmarkTest', num_demo_participants=None, app_sequence=['FirmBehaviorBenchmark'], use_browser_bots=True), dict(name='SSTest', num_demo_participants=None, app_sequence=['FirmBehaviorSearchSignal'], use_browser_bots=True)]
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = []
SESSION_FIELDS = []
ROOMS = [dict(name='Benchmark', display_name='Firm Behavior Game')]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = 'blahblah'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']



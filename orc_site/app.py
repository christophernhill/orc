import os
# import logging
from flask import Flask, render_template, request, redirect
# app = Flask(__name__, template_folder='../templates/orc_site')
app = Flask(__name__)


context = {
    'version': 'beta',
    'test_version': 'test-beta',
    'home_url': '/',
    'jhub_url': '/hub/',
    'logout_url': '/hub/logout',
    'gesis_login_url': 'https://notebooks{}.gesis.org/Shibboleth.sso/Login?SAMLDS=1&'
                       'target=https://notebooks{}.gesis.org/hub/login&'
                       'entityID=https%3A%2F%2Fidp.gesis.org%2Fidp%2Fshibboleth'.
                       format(*['-test', '-test'] if os.environ.get('DEPLOYMENT_ENV') == 'staging' else ['', '']),
    'bhub_url': '/services/binder/',
    'about_url': '/about/',
    'tou_url': '/terms_of_use/',
    'imprint_url': 'https://www.gesis.org/en/institute/imprint/',
    'data_protection_url': 'https://www.gesis.org/en/institute/data-protection/',
    'contact_url': 'mailto:notebooks@gesis.org',
    'gesis_url': 'https://www.gesis.org/en/home/',
    'help_url': 'https://www.gesis.org/en/help/',
    'shibboleth_entityID': 'https://notebooks.gesis.org/shibboleth',
    'test_shibboleth_entityID': 'https://notebooks-test.gesis.org/shibboleth',
    'is_staging': os.environ.get('DEPLOYMENT_ENV') == 'staging',
    'is_production': os.environ.get('DEPLOYMENT_ENV') == 'production'
}


def user_logged_in():
    for cookie_name in request.cookies:
        if cookie_name.startswith('_shibsession'):
            return True
    return False


@app.errorhandler(404)
def not_found(error):
    context.update({'status_code': error.code,
                    'status_message': error.name,
                    'message': error.description,
                    'active': None,
                    'login_required': not user_logged_in()})
    return render_template('error.html', **context), 404


@app.route('/')
def home():
    if user_logged_in():
        # logger = logging.getLogger('werkzeug')
        app.logger.info('User already logged in, redirecting to JupyterHub {}'.format(context['jhub_url']))
        return redirect(context['jhub_url'])

    # domain = 'https://notebooks{}.gesis.org'.format('-test' if os.environ.get('DEPLOYMENT_ENV') == 'staging' else '')
    # binder_examples = [
    #     {'headline': 'Girls Day Hackathon',
    #      'content': '',
    #      'binder_link': '{}{}v2/gh/gesiscss/workshop_girls_day/master'.format(domain, context['bhub_url']),
    #      'repo_link': 'https://github.com/gesiscss/workshop_girls_day'},
    #     {'headline': 'Python Data Science Handbook',
    #      'content': '',
    #      'binder_link': '{}{}v2/gh/gesiscss/PythonDataScienceHandbook/master'.format(domain, context['bhub_url']),
    #      'repo_link': 'https://github.com/gesiscss/PythonDataScienceHandbook'},
    #     {'headline': 'LIGO Binder',
    #      'content': '',
    #      'binder_link': '{}{}v2/gh/minrk/ligo-binder/master'.format(domain, context['bhub_url']),
    #      'repo_link': 'https://github.com/minrk/ligo-binder'},
    # ]
    context.update({'active': 'home',
                    'login_required': True})
    return render_template('home.html', **context)


@app.route('/about/')
def about():
    context.update({'active': 'about', 'login_required': not user_logged_in()})
    return render_template('about.html', **context)


@app.route('/terms_of_use/')
def terms_of_use():
    context.update({'active': 'terms_of_use', 'login_required': not user_logged_in()})
    return render_template('terms_of_use.html', **context)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')

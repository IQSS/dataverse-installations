if __name__ == '__main__':
    import os, sys
    import django
    from os.path import realpath, dirname
    proj_path = dirname(dirname(realpath(__file__)))

    sys.path.append(proj_path)
    sys.path.append(dirname(proj_path))
    django.setup()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "miniverse.settings.local")

from apps.dataverses.models import Dataverse, CitationPageCheck
import requests


class CitationURLChecker(object):
    """
    For all Dataverse objects with a citationRedirectUrl
        - Go to the "citation_redirect_url" page
        - Make sure the page contains the dataverse widget
    that the "citation_redirect_url"
    """
    def __init__(self, dataverse, contact_email, dataverse_site_url='https://dataverse.harvard.edu'):
        if dataverse is None:
            raise Exception('The dataverse cannot be None')
        if not dataverse.citation_redirect_url:
            raise Exception('This dataverse (%s) does not have a citation_redirect_url' % (dataverse.name))

        if dataverse_site_url is None or len(dataverse_site_url) == 0:
            raise Exception('The dataverse_site_url cannot be None')

        self.dataverse_site_url = self.format_site_url(dataverse_site_url)
        self.dataverse = dataverse
        self.contact_email = contact_email

        self.widget_found = False
        self.err_found = False
        self.err_list = []

        # widget link to check for
        self.widget_link = None

        # start "log" -- object to save results
        self.citation_page_check = CitationPageCheck(dataverse=self.dataverse,
                    citation_url=self.dataverse.citation_redirect_url)


        self.check_page_for_widget_url()

    def format_site_url(self, site_url):
        if site_url is None or len(site_url) == 0:
            self.add_error('The site_url is not valid: %s' % site_url)
            return site_url

        if site_url.endswith('/'):
            return site_url[:-1]
        return site_url

    def add_error(self, err_msg):
        self.err_found = True
        self.err_list.append(err_msg)

    def get_error_message(self, delim='\n'):
        return delim.join(self.err_list)

    def set_widget_link(self):

        self.widget_link = '%s/resources/js/widgets.js?alias=%s' % \
            (self.dataverse_site_url, self.dataverse.alias)

        # save to db
        self.citation_page_check.widget_link = self.widget_link
        self.citation_page_check.save()

    def check_page_for_widget_url(self):
        """
        Go through the process of checking for the widget
        and recording the results
        """
        if self.err_found:
            return False

        citation_url = self.dataverse.citation_redirect_url

        self.set_widget_link()

        # Get the citation page
        try:
            resp = requests.get(citation_url)
        except requests.exceptions.ConnectionError:
            self.add_error('ConnectionError. Failed to retrieve citation url content. Make sure site exists: %s' % citation_url)
            self.save_citation_page_check(with_error=True)
            return False
        except requests.exceptions.Timeout:
            self.add_error('Timeout Error. Failed to retrieve citation url content: %s' % citation_url)
            self.save_citation_page_check(with_error=True)
            return False
        except requests.exceptions.InvalidURL:
            self.add_error('InvalidURL. The citation url was invalid: %s' % citation_url)
            self.save_citation_page_check(with_error=True)
            return False
        except:
            self.add_error('Failed to retrieve citation url content: %s' % citation_url)
            self.save_citation_page_check(with_error=True)
            return False

        # Did the page request work?
        if resp.status_code != 200:
            self.add_error('Failed to retrieve citation url content: %s. Status code: %s' % (citation_url, resp.status_code))
            self.save_citation_page_check(with_error=True)
            return False

        # Found widget in page!
        html_content = resp.content.decode('utf-8')
        if html_content.find(self.widget_link) > -1:
            self.widget_found = True
            self.save_citation_page_check(with_error=False)
            return True
        else:
            self.add_error('Failed to find widget link in page: %s\nWidget checked for: %s' %\
                (citation_url, self.widget_link))
            self.save_citation_page_check(with_error=True)
            return False

    def save_citation_page_check(self, with_error=False):

        if with_error:
            self.citation_page_check.error_message = self.get_error_message()
            self.citation_page_check.citation_found = False
        else:
            self.citation_page_check.citation_found = True
        self.citation_page_check.save()

if __name__ == '__main__':
    dv = Dataverse.objects.get(pk=1)
    cc = CitationURLChecker(dv, 'raman_prasad@harvard.edu')

"""
<textarea rows="3" cols="54" class="form-control">&lt;script src=&quot;#{systemConfig.dataverseSiteUrl}/resources/js/widgets.js?alias=#{themeWidgetFragment.editDv.alias}&amp;amp;dvUrl=#{systemConfig.dataverseSiteUrl}&amp;amp;widgetScope=#{themeWidgetFragment.editDv.alias}&amp;amp;widget=iframe&amp;amp;heightPx=500&quot;&gt;&lt;/script&gt;</textarea>
"""
"""
from apps.dataverses.citation_url_checker import CitationURLChecker
from apps.dataverses.models import Dataverse
dv = Dataverse.objects.get(pk=1)
cc = CitationURLChecker(dv, 'raman_prasad@harvard.edu')
"""

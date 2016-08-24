"""
Middleware to restrict the admin by IP address
"""
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404

class RestrictAdminMiddleware(object):
    """
    Simple middlware to only accept admin requests coming from internal IPs
    based on: http://djangosnippets.org/snippets/2095/
    """

    def process_request(self, request):
        try:
            # Get the admin url
            admin_index = reverse('admin:index')
        except NoReverseMatch:
            # No admin url exists, all set
            return

        # This isn't an admin request, all set
        if not request.path.startswith(admin_index):
            return

        # -------------------------------------------
        # OK, this is a call to the admin
        # Try to get the remote address from headers:
        #   - HTTP_X_REAL_IP or
        #   - REMOTE_ADDR
        # -------------------------------------------
        remote_addr = request.META.get('HTTP_X_REAL_IP',\
                      request.META.get('REMOTE_ADDR', None))

        # -------------------------------------------
        # No remote address, sorry, no access!
        # -------------------------------------------
        if remote_addr is None:
            # We're not even here...
            raise Http404('remote_addr: %s' % remote_addr)

        #--------------------------------------------------------
        # Is this an INTERNAL_IP address?
        #--------------------------------------------------------
        if remote_addr in settings.INTERNAL_IPS:
            # Yes!  Looking good, looking good.
            return

        #--------------------------------------------------------
        #  Also acceptable if INTERNAL_IP listing is two segments
        #   and those match.
        #   For HU, this is 140.147 and allow internal 10.1 settings
        #--------------------------------------------------------
        remote_addr_pieces = remote_addr.split('.')
        print 'remote_addr_pieces', remote_addr_pieces
        if len(remote_addr_pieces) == 4:
            if '.'.join(remote_addr_pieces[:2]) in settings.INTERNAL_IPS:
                # Yes! 1st two segments match. Looking good, looking good.
                return
            elif '.'.join(remote_addr_pieces[:3]) in settings.INTERNAL_IPS:
                # Yes! 1st three segments match. Looking good, looking good.
                return

        #--------------------------------------------------------
        # You ain't got a thing, if you ain't got that admin
        # (no address match, show a 404)
        #--------------------------------------------------------
        raise Http404('remote_addr: %s' % remote_addr)

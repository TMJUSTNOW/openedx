"""
Decorators for Mobile APIs.
"""
import functools
from rest_framework import status
from rest_framework.response import Response

from lms.djangoapps.courseware.courses import get_course_with_access
from lms.djangoapps.courseware.courseware_access_exception import CoursewareAccessException
from mobile_api.models import MobileAvailableConfig
from opaque_keys.edx.keys import CourseKey
from xmodule.modulestore.django import modulestore


def mobile_course_access(depth=0):
    """
    Method decorator for a mobile API endpoint that verifies the user has access to the course in a mobile context.
    """
    def _decorator(func):
        """Outer method decorator."""

        @functools.wraps(func)
        def _wrapper(self, request, *args, **kwargs):
            """
            Expects kwargs to contain 'course_id'.
            Passes the course descriptor to the given decorated function.
            Raises 404 if access to course is disallowed.
            """
            course_id = CourseKey.from_string(kwargs.pop('course_id'))
            with modulestore().bulk_operations(course_id):
                try:
                    if MobileAvailableConfig.ignore_mobile_available_flag():
                        action = "load"
                    else:
                        action = "load_mobile"

                    course = get_course_with_access(
                        request.user,
                        action,
                        course_id,
                        depth=depth,
                        check_if_enrolled=True,
                    )
                except CoursewareAccessException as error:
                    return Response(data=error.to_json(), status=status.HTTP_404_NOT_FOUND)
                return func(self, request, course=course, *args, **kwargs)

        return _wrapper
    return _decorator

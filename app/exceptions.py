from fastapi import HTTPException, status


class AppException(HTTPException):
    pass


class TeamExistsException(AppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "TEAM_EXISTS", "message": "team_name already exists"}
        )


class PRExistsException(AppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "PR_EXISTS", "message": "PR id already exists"}
        )


class PRMergedException(AppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "PR_MERGED", "message": "cannot reassign on merged PR"}
        )


class NotAssignedException(AppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "NOT_ASSIGNED", "message": "reviewer is not assigned to this PR"}
        )


class NoCandidateException(AppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "NO_CANDIDATE", "message": "no active replacement candidate in team"}
        )


class NotFoundException(AppException):
    def __init__(self, resource: str = "resource"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": f"{resource} not found"}
        )


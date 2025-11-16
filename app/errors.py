from fastapi import HTTPException


class ApiError:
    @staticmethod
    def not_found(msg="not found"):
        raise HTTPException(status_code=404, detail={
            "error": {"code": "NOT_FOUND", "message": msg}
        })

    @staticmethod
    def team_exists():
        raise HTTPException(status_code=400, detail={
            "error": {"code": "TEAM_EXISTS", "message": "team_name already exists"}
        })

    @staticmethod
    def pr_exists():
        raise HTTPException(status_code=409, detail={
            "error": {"code": "PR_EXISTS", "message": "PR id already exists"}
        })

    @staticmethod
    def pr_merged():
        raise HTTPException(status_code=409, detail={
            "error": {"code": "PR_MERGED", "message": "cannot reassign on merged PR"}
        })

    @staticmethod
    def not_assigned():
        raise HTTPException(status_code=409, detail={
            "error": {"code": "NOT_ASSIGNED", "message": "reviewer is not assigned to this PR"}
        })

    @staticmethod
    def no_candidate():
        raise HTTPException(status_code=409, detail={
            "error": {"code": "NO_CANDIDATE", "message": "no active replacement candidate in team"}
        })

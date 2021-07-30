import datetime
from django.db import connection
from common.read_logger import LoggerSetup


class StoredProcedure:
    def __init__(self):
        self.logger = LoggerSetup(loggerName=str(__file__)).getLogger()

    def fetch_approval_status_by_mentor(self, *args):
        """
        CREATE OR ALTER PROCEDURE ImdAttendanceStatusByMentor @FetchedMentorName nvarchar(50)
        AS

        SELECT t1.UserID,CONCAT(t2.FirstName,' ',t2.MiddleName,' ',t2.LastName) as FullName,t1.CheckIn,t1.CheckOut,t1.ApprovalStatus, t1.CreatedOn FROM dbo.UserAttendanceLogs t1 left join
        dbo.UserDetails t2 ON t2.UserID = t1.UserID WHERE t1.ApprovalStatus = 'Pending' and t2.Mentor = @FetchedMentorName and t1.CheckOut is not NULL

        GO
        """

        def date_filter(input_data_point):
            if isinstance(input_data_point, datetime.datetime):
                return input_data_point.__str__()
            return input_data_point

        with connection.cursor() as cursor:
            cursor.execute(
                f"EXEC ImdAttendanceStatusByMentor @FetchedMentorName='{args[0]}'"
            )
            columns = [col[0] for col in cursor.description]
            data = [
                dict(zip(columns, [date_filter(element) for element in row]))
                for row in cursor.fetchall()
            ]
        self.logger.info("Ran 'EXEC ImdAttendanceStatusByMentor' in database")
        return data

    def fetch_attendance_pagination(
        self, pagenumber: int, userid: str, size: int = 10
    ) -> dict:
        """
        CREATE OR ALTER PROCEDURE usp_ImdAttendancePagination @size INT, @pagenumber INT, @userid nvarchar(50)
        AS
        BEGIN
            SELECT * FROM dbo.UserAttendanceLogs WHERE UserID = @userid ORDER BY CreatedOn desc OFFSET (@size*(@pagenumber-1)) ROWS FETCH NEXT @size ROWS ONLY
        END
        GO
        """

        def date_filter(input_data_point):
            if isinstance(input_data_point, datetime.datetime):
                return input_data_point.__str__()
            return input_data_point

        with connection.cursor() as cursor:
            cursor.execute(
                f"EXEC usp_ImdAttendancePagination @pagenumber={pagenumber}, @size={size}, @userid={userid}"
            )
            columns = [col[0] for col in cursor.description]
            data = [
                dict(zip(columns, [date_filter(element) for element in row]))
                for row in cursor.fetchall()
            ]
        self.logger.info("Ran 'EXEC ImdAttendanceStatusByMentor' in database")
        return data


class Queries:
    def __init__(self):
        self.logger = LoggerSetup(loggerName=str(__file__)).getLogger()

    def fetch_total_number_of_records(self, userid: str) -> int:
        with connection.cursor() as cursor:
            cursor.execute(
                "select count(*) from dbo.UserAttendanceLogs where UserID='%s'" % userid
            )
            result = cursor.fetchone()
        return result[0]

    def fetch_all_attendance_records_by_user(self, userid: str) -> list:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM dbo.UserAttendanceLogs WHERE UserID = '%s' ORDER BY CreatedOn desc"
                % userid
            )
            columns = [col[0] for col in cursor.description]
            data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return data
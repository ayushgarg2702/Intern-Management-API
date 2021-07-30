import datetime
from django.db import connection
from common.read_logger import LoggerSetup


class StoredProcedure:
    def __init__(self):
        self.logger = LoggerSetup(loggerName=str(__file__)).getLogger()

    def fetch_interns_under_mentor(self, mentor: str):
        """
        CREATE PROCEDURE usp_ImdInternsListAsPerMentor @Mentor nvarchar(50)
        AS
        BEGIN
            SELECT UserID,UserStatus, Mentor, CurrentProject, CONCAT(FirstName,' ',MiddleName,' ',LastName) AS FullName FROM dbo.UserDetails WHERE Mentor = @Mentor
        END
        GO
        """

        def date_filter(input_data_point):
            if isinstance(input_data_point, datetime.datetime):
                return input_data_point.__str__()
            return input_data_point

        with connection.cursor() as cursor:
            cursor.execute(f"EXEC usp_ImdInternsListAsPerMentor @Mentor='{mentor}'")
            columns = [col[0] for col in cursor.description]
            data = [
                dict(zip(columns, [date_filter(element) for element in row]))
                for row in cursor.fetchall()
            ]
        self.logger.info("Ran 'EXEC usp_ImdInternsListAsPerMentor' in database")
        return data

    def fetch_all_interns(self, size: int, pagenumber: int):
        """
        CREATE OR ALTER PROCEDURE usp_ImdInternDetailsPagination @size INT, @pagenumber INT
        AS
        BEGIN
            SELECT UserID,UserStatus, Mentor, CurrentProject, CONCAT(FirstName,' ',MiddleName,' ',LastName) AS FullName FROM dbo.UserDetails ORDER BY FullName OFFSET (@size*(@pagenumber-1)) ROWS FETCH NEXT @size ROWS ONLY
        END
        GO
        """
        with connection.cursor() as cursor:
            cursor.execute(
                f"EXEC usp_ImdInternDetailsPagination @pagenumber=%(pagenumber)s, @size=%(size)s"
                % {"pagenumber": pagenumber, "size": size}
            )
            columns = [col[0] for col in cursor.description]
            data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        self.logger.info("Ran 'EXEC usp_ImdInternsListAsPerMentor' in database")
        return data


class Queries:
    def __init__(self):
        self.logger = LoggerSetup(loggerName=str(__file__)).getLogger()

    def fetch_all_interns(self):
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT UserID,UserStatus, Mentor, CurrentProject, CONCAT(FirstName,' ',MiddleName,' ',LastName) AS FullName FROM dbo.UserDetails"
            )
            columns = [col[0] for col in cursor.description]
            data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        self.logger.info("Ran fetch_all_interns query")
        return data
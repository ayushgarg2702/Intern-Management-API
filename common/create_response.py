def create_failure( message, reply_code):
    output = {
        'Message' : message,
        'ReplyCode' : reply_code,
        'Data' : {}
        }
    return output

def create_success(message, data = {}):
    output = {
        'Message' : message,
        'ReplyCode' : 'Success',
        'Data' : data
    }
    return output
from AutomationFramework.common.db.crud import testcase_crud, server_crud, interface_crud
from AutomationFramework.schemas import testcase_schemas, server_schemas
from AutomationFramework.middleware.http_client import Request


def obtain_the_api_testcase_to_be_executed(testcase, current_user):
    """
    获取待执行接口用例
    :param testcase:
    :param current_user:
    :return:
    """
    return testcase_crud.get_testcase_to_be_executed(testcase, current_user)


def assemble_the_request(testcase: testcase_schemas.TestCaseInfo, server_path=None):
    '''
    拼接请求体
    :param testcase:
    :param server_path:
    :return:
    '''
    # 判断是否有关联用例，有关联用例时，优先执行关联用例
    if testcase.related_case is not None:
        related_case = testcase_crud.get_testcase_by_id(testcase.related_case)
        assemble_the_request(related_case)
    interface = interface_crud.get_interface_by_id(testcase.interface_id)
    server = server_crud.get_serverinfo_by_id(
        server_id=server_path if server_path is not None else testcase.server_path)
    result = testcase_schemas.BuildInterfaceTestCases
    result.url = fr"{interface['protocol']}://{server['ip']:{server['port']}}{interface['url']}"
    if testcase.headers is not None:
        result.headers.update(testcase.headers)
    if interface.headers is not None:
        result.headers.update(interface.headers)
    result.method = interface['method'].upper()
    if interface['type'] == 0:
        result.params = testcase.parameters
    elif interface['type'] == 1:
        result.data = testcase.parameters
    elif interface['type'] == 3:
        result.json = testcase.parameters
    else:
        result.files = testcase.parameters
    return result


def executed_testcase(data: testcase_schemas.ExecuteInterfaceTestCases, current_user):
    """
    执行接口用例，并返回执行数据
    :param data:
    :param current_user:
    :return:
    """

    result = testcase_schemas.TestCaseExecutionReport
    testcases = obtain_the_api_testcase_to_be_executed(data, current_user)
    result.total_num = len(testcases)
    result.create_user = current_user.id
    result.update_user = current_user.id
    result.belong_project = data.belong_project
    success_num = 0
    fail_num = 0
    skip_num = 0
    for testcase in testcases:
        if testcase.related_case is not None:
            pass
        body = assemble_the_request(testcase, data.belong_project)
        r = Request(**body.dict())
        response = r.request(body.method)

        if response.status_code != 200:
            fail_num += 1
        else:
            success_num += 1

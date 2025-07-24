<?php
function fail($code = 1, $msg = 'fail', $data = '', $json = false) {
    header('Content-type', 'application/json');
    echo json_encode(array('code' => $code, 'msg' => $msg, 'data' => $data));
    exit;
}

function load() {
    // 输入参数校验
    $key = isset($_POST['key']) ? urlencode($_POST['key']) : '';

    if (!$key) {
        fail(1, 'error', '参数不能为空');
    }

    $db_username = SAE_MYSQL_USER;
    $db_password = SAE_MYSQL_PASS;
    $db_host = SAE_MYSQL_HOST_M;
    $db_port = SAE_MYSQL_PORT;
    $db_name = SAE_MYSQL_DB;
    $dsn = "mysql:host={$db_host};port={$db_port};dbname={$db_name}";
    $options = array(
        PDO::MYSQL_ATTR_INIT_COMMAND => 'SET NAMES utf8',
    );

    try {
        $db = new PDO($dsn, $db_username, $db_password, $options);

        if (!$db) {
            fail(1, 'fail', '无法读取[1]');
        }

        $sql = 'SELECT `data` FROM `record` WHERE `key` = ?';
        $stmt = $db->prepare($sql);
        $stmt->execute(array($key));
        $found = $stmt->fetchAll(PDO::FETCH_ASSOC);

        if ($found) {
            header('Content-type', 'application/json');
            echo json_encode(array('code' => 1, 'msg' => 'success', 'data' => $found[0]['data']));
        }
        else {
            header('Content-type', 'application/json');
            echo json_encode(array('code' => 0, 'msg' => 'notfound', 'data' => '不存在该存档。'));
        }

    }
    catch (Exception $e) {
        fail(1, 'fail', '无法读取[2]');
    }
}

load();

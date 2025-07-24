<?php
function fail($code = 1, $msg = 'error', $data = '', $json = false) {
	header('Content-type', 'application/json');
    echo json_encode(array('code' => $code, 'msg' => $msg, 'data' => $data));
    exit;
}

function save() {
    // 输入参数校验
    $key = isset($_POST['key']) ? urlencode($_POST['key']) : '';
    $data = isset($_POST['data']) ? ($_POST['data']) : '';
    $username = isset($_POST['username']) ? ($_POST['username']) : '';
    $overwrite = isset($_POST['overwrite']) ? ($_POST['overwrite']) : '';

    if (!$key || !$data) {
        fail(1, 'error', '参数不能为空');
    }

    if (!json_decode($data, true)) {
        fail(1, 'error', '存档数据格式不正确');
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

    $save_result = false;

    try {
        $db = new PDO($dsn, $db_username, $db_password, $options);

        if (!$db) {
            fail(1, 'fail', '无法存档[1]');
        }

        $sql = 'SELECT `username` FROM `record` WHERE `username` = ? AND `key` != ?';
        $stmt = $db->prepare($sql);
        $stmt->execute(array($username, $key));
        $found = $stmt->fetchAll(PDO::FETCH_ASSOC);

        if ($found) {
			header('Content-type', 'application/json');
            echo json_encode(array('code' => 2,'msg' => 'repeated'));
            exit;
        }
        else {
            $sql = 'SELECT `key` FROM `record` WHERE `key` = ?';
            $stmt = $db->prepare($sql);
            $stmt->execute(array($key));
            $found = $stmt->fetchAll(PDO::FETCH_ASSOC);
            if ($found) {
                $sql = 'UPDATE `record` SET `username` = ?, `data` = ?  WHERE `key` = ?';
                $stmt = $db->prepare($sql);
                $ret = $stmt->execute(array($username, $data, $key));

                if ($ret) {
                    $save_result = true;
                }
            }
            else{
                $sql = 'INSERT INTO `record`(`key`, `username`, `data`) VALUES(?, ?, ?)';
                $stmt = $db->prepare($sql);
                $ret = $stmt->execute(array($key, $username, $data));

                if ($ret) {
                    $save_result = true;
                }
            }
        }

    }
    catch (Exception $e) {
        fail(-2, 'fail', '无法存档。');
    }

    if ($save_result) {
        header('Content-type', 'application/json');
        echo json_encode(array('code' => 1, 'msg' => 'success'));
    }
    else {
        fail(-1, 'fail', '存档写入失败。');
    }
}

save();

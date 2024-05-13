import threading

import casbin  # type: ignore
import casbin_sqlalchemy_adapter  # type: ignore
from casbin_rabbitmq_watcher import new_watcher  # type: ignore

from config import (MYSQL_URL, RABBITMQ_HOST, RABBITMQ_PASSWORD, RABBITMQ_PORT,
                    RABBITMQ_USER)

adapter = casbin_sqlalchemy_adapter.Adapter(MYSQL_URL)
watcher = new_watcher(RABBITMQ_HOST, RABBITMQ_PORT,
                      username=RABBITMQ_USER, password=RABBITMQ_PASSWORD)

enforcer = casbin.Enforcer('casbin-model.conf', adapter)


def watch_cb(msg):
    threading.Thread(target=enforcer.load_policy).start()


def create_default_policies():
    p = [
        ['role_admin', '/policy', '(read|write|delete)'],
        ['role_admin', '/role', '(read|write|delete)'],
        ['role_admin', '/asmre/student', '(create|update|delete)'],
        ['role_admin', '/asmre/student/:name',
            '(create|update|delete)'],
        ['role_admin', '/asmre/credit/:name', '(create|update|delete)'],
    ]

    enforcer.add_policies(p)


watcher.set_update_callback(watch_cb)
enforcer.set_watcher(watcher)
enforcer.add_named_matching_func('g2', 'keyMatch2')

enforcer.load_policy()
enforcer.enable_auto_save(True)

create_default_policies()

__all__ = ['enforcer']

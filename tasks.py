import os

from invoke import Collection, tasks
from invoke.util import LOG_FORMAT

from steem import command as steem_cmd
from blog import command as blog_cmd


def add_tasks_in_module(mod, ns):
    functions = [(name, val) for name, val in mod.__dict__.items() if callable(val)]
    for (name, method) in functions:
        # only add the method if it's of type invoke.tasks.Task
        if type(method) == tasks.Task:
            ns.add_task(method, name)
    return ns

steem_ns = add_tasks_in_module(steem_cmd, Collection('steem'))
blog_ns = add_tasks_in_module(blog_cmd, Collection('blog'))

ns = Collection(
    steem_ns,
    blog_ns
)

ns.configure({'conflicted': 'default value'})

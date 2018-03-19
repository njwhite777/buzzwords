#!/usr/bin/env python


import rethinkdb as r
from tornado import ioloop, gen

r.set_loop_type("tornado")

@gen.coroutine
def print_changes():
    conn = yield r.connect(host="localhost",port=28015,db="buzzwords")
    feed = yield r.table("games").changes().run(conn)
    while (yield feed.fetch_next()):
        change = yield feed.next()
        print(change)

loop=ioloop.IOLoop.current()
loop.add_callback(print_changes)
loop.start()

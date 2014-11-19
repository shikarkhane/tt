tt
==

communication app

Examples of data structures in redis store

1. [Message( read gif1 and "hello") from user A to user B @ 20141112101523]
will be stored in hash map

set A:B:20141112101523 "gif1|hello"

lpush sender:A:user "A:B:20141112101523"
lpush receiver:B:user "A:B:20141112101523"
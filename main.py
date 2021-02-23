# credits to graingert

import asyncio
import anyio
import sys
from qasync import QEventLoop

from PyQt5.QtWidgets import QApplication


class QEventLoopPolicyMixin:
    def new_event_loop(self):
        return QEventLoop(QApplication(sys.argv))


class DefaultQEventLoopPolicy(QEventLoopPolicyMixin, asyncio.DefaultEventLoopPolicy):
    pass


@contextlib.contextmanager
def set_event_loop_policy(policy):
    old_policy = asyncio.get_event_loop_policy()
    asyncio.set_event_loop_policy(policy)
    try:
        yield
    finally:
        asyncio.set_event_loop_policy(old_policy)


def qasync_run(*args, **kwargs):
    with set_event_loop_policy(DefaultQEventLoopPolicy()):
        return asyncio.run(*args, **kwargs)


async def amain():
    async with anyio.create_task_group() as tg:
        mainWindow = MainWindow(tg)
        mainWindow.show()
    return 0


if __name__ == "__main__":
    sys.exit(qasync_run(amain()))

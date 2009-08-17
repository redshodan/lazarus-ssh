/*
  Borrowed code from openssh. Original license follows. 
 */

/* $OpenBSD: monitor_fdpass.c,v 1.18 2008/11/30 11:59:26 dtucker Exp $ */
/*
 * Copyright 2001 Niels Provos <provos@citi.umich.edu>
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
 * IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 * IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 * NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
 * THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/uio.h>

#include <errno.h>
#include <string.h>
#include <stdarg.h>

#include <Python.h>

static PyObject* sendfd(PyObject *self, PyObject *args, PyObject *keywds)
{
    int sock, fd;
	struct msghdr msg;
	union {
		struct cmsghdr hdr;
		char buf[CMSG_SPACE(sizeof(int))];
	} cmsgbuf;
	struct cmsghdr *cmsg;
	struct iovec vec;
	char ch = '\0';
	ssize_t n;

    if (!PyArg_ParseTuple(args, "ii", &sock, &fd))
    {
        return NULL;
    }

	memset(&msg, 0, sizeof(msg));
	msg.msg_control = (caddr_t)&cmsgbuf.buf;
	msg.msg_controllen = sizeof(cmsgbuf.buf);
	cmsg = CMSG_FIRSTHDR(&msg);
	cmsg->cmsg_len = CMSG_LEN(sizeof(int));
	cmsg->cmsg_level = SOL_SOCKET;
	cmsg->cmsg_type = SCM_RIGHTS;
	*(int *)CMSG_DATA(cmsg) = fd;

	vec.iov_base = &ch;
	vec.iov_len = 1;
	msg.msg_iov = &vec;
	msg.msg_iovlen = 1;

	while ((n = sendmsg(sock, &msg, 0)) == -1 && (errno == EAGAIN ||
	    errno == EINTR))
		printf("%s: sendmsg(%d): %s", __func__, fd, strerror(errno));
	if (n == -1) {
        PyErr_SetFromErrno(PyExc_OSError);
		return NULL;
	}

	if (n != 1) {
		printf("%s: sendmsg: expected sent 1 got %ld",
		    __func__, (long)n);
		return NULL;
	}

    Py_INCREF(Py_None);
    return Py_None;
}

static PyMethodDef methods[] = 
{
    {"sendfd", (PyCFunction)sendfd, METH_VARARGS, "sendfd(sock, fd)"},
    {NULL, NULL, 0, NULL}
};

void initsendfd(void)
{
    Py_InitModule("sendfd", methods);
}

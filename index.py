#!/usr/bin/env python

import logging
import cgi

import warnings
warnings.filterwarnings('ignore', '.*the sets module is deprecated.*',
                        DeprecationWarning, 'MySQLdb')

import MySQLdb as mdb

def extend_welcome():
	print "Content-Type: text/xml"
	print
	print """<?xml version="1.0" encoding="UTF-8"?>
	<Response>
	    <Gather action="http://www.williamslabs.com/gatekeeper/index.py" method="POST" timeout="10" numDigits="4" />
	    <Say voice="woman">Extension not received, goodbye</Say>
	    <Hangup/>
	</Response>
	"""

def extend_access(gate_id):
	con = mdb.connect('pwilliamsttrss.db', 'pwilliams', 'password', 'gatekeeper')
	cur = con.cursor()
	cur.execute("SELECT access_message, access_code FROM gates WHERE extension = %d" % (gate_id))
	message, code = cur.fetchone()
	print "Content-Type: text/xml"
	print
	print """<?xml version="1.0" encoding="UTF-8"?>
	<Response>
	    <Say voice="woman">%s</Say>
	    <Play digits="%s" />
	    <Hangup/>
	</Response>
	""" % (message, code)

def extend_denial(gate_id):
	con = mdb.connect('pwilliamsttrss.db', 'pwilliams', 'password', 'gatekeeper')
	cur = con.cursor()
	cur.execute("SELECT denial_message FROM gates WHERE extension = %d" % (gate_id))
	message = cur.fetchone()[0]
	print "Content-Type: text/xml"
	print
	print """<?xml version="1.0" encoding="UTF-8"?>
	<Response>
	    <Say voice="woman">%s</Say>
	    <Hangup/>
	</Response>
	""" % (message)

def extend_forward(source, gate_id):
	con = mdb.connect('pwilliamsttrss.db', 'pwilliams', 'password', 'gatekeeper')
	cur = con.cursor()
	cur.execute("SELECT forward_number FROM gates WHERE extension = %d" % (gate_id))
	number = cur.fetchone()[0]
	print "Content-Type: text/xml"
	print
	print """<?xml version="1.0" encoding="UTF-8"?>
	<Response>
	    <Dial timeLimit="60" callerId="%s">%s</Dial>
	    <Hangup/>
	</Response>
	""" % (source, number)

def extend_unknown():
	print "Content-Type: text/xml"
	print
	print """<?xml version="1.0" encoding="UTF-8"?>
	<Response>
	    <Hangup/>
	</Response>"""

def log_call(sid, action, ext=-1):
	con = mdb.connect('pwilliamsttrss.db', 'pwilliams', 'password', 'gatekeeper')
	cur = con.cursor()
	logging.info(sid)
	logging.info(action)
	if ext == -1:
	    cur.execute("INSERT INTO log (sid, action, time) VALUES ('%s', '%s', NOW())" % (sid, action))
	else:
	    cur.execute("INSERT INTO log (sid, action, extension, time) VALUES ('%s', '%s', '%s', NOW())" % (sid, action, ext))

def handle_extension(call_sid, source, gate_id):
	con = mdb.connect('pwilliamsttrss.db', 'pwilliams', 'password', 'gatekeeper')
	cur = con.cursor()
	num = cur.execute("SELECT state FROM gates WHERE extension = %d" % (gate_id))

	if num != 1:
    	    log_call(call_sid, 'unknown_extension', gate_id)
	    extend_unknown()
	else:
	    state = cur.fetchone()[0]
	    if state == 'allow':
    	        log_call(call_sid, 'allow', gate_id)
		extend_access(gate_id)
	    elif state == 'deny':
    	        log_call(call_sid, 'deny', gate_id)
		extend_denial(gate_id)
	    elif state == 'forward':
    	        log_call(call_sid, 'forward', gate_id)
		extend_forward(source, gate_id)


# 1. Lookup account associated with source phone number
# 2. Determine whether to open based on current account settings
# 3. Return accept or deny message to twilio

logging.basicConfig(filename='/home/logs/gatekeeper_log',level=logging.DEBUG)

form = cgi.FieldStorage()
logging.info(form)

call_sid = form.getvalue('CallSid')
#received_account_sid = form.getvalue('AccountSid')
call_from = form.getvalue('From')
call_to = form.getvalue('To')

#logger.info(call_sid, received_account_sid, call_from, call_to)

if form.has_key('Digits'):
    gate_id = int(form.getvalue('Digits'))
    logging.info(gate_id)
    handle_extension(call_sid, call_from, gate_id)
else:
    log_call(call_sid, 'welcome')
    extend_welcome()


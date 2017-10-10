"""Unit test for database module."""
import inspect
import os
import sys
import test_utils
import unittest

# Needed to import custom modules from parent directory
currentdirectory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdirectory = os.path.dirname(currentdirectory)
sys.path.insert(0, parentdirectory)
import batch
import database
import event


class TestEventModule(unittest.TestCase):
    """Class to execute unit tests for database.py."""

    @classmethod
    def setUpClass(self):
        """Set up function called when class is consructed."""
        self.testcaselist = []

    def test_logevent_sessionstart(self):
        """Test log event function with session start event."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append(testcasename)

        # Create batch owner
        with database.Function('BatchOwner') as function:
            batchownerlist = function.create(name=testcasename)

        # Create data quality indicator
        with database.Function('Indicator') as function:
            indicatorlist = function.create(
                name=testcasename,
                description=testcasename,
                indicatorTypeId=1,
                batchOwnerId=batchownerlist[0].id,
                executionOrder=0,
                alertOperator='=',
                alertThreshold='0',
                distributionList=testcasename,
                active=True)

        # Start batch
        batchrecord = batch.logbatch(testcasename, 'Batch start')

        # Start session
        sessionstartevent = event.logevent(indicatorlist[0].id, batchrecord.id, 'Session start')

        # Get session
        with database.Function('Session') as function:
            sessionlist = function.read(indicatorId=indicatorlist[0].id, batchId=batchrecord.id)

        self.assertEqual(sessionlist[0].statusId, 1)
        self.assertEqual(sessionstartevent.eventTypeId, 1)
        self.assertEqual(sessionstartevent.sessionId, sessionlist[0].id)

    def test_logevent_sessionstop(self):
        """Test log event function with session stop event."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append(testcasename)

        # Create batch owner
        with database.Function('BatchOwner') as function:
            batchownerlist = function.create(name=testcasename)

        # Create data quality indicator
        with database.Function('Indicator') as function:
            indicatorlist = function.create(
                name=testcasename,
                description=testcasename,
                indicatorTypeId=1,
                batchOwnerId=batchownerlist[0].id,
                executionOrder=0,
                alertOperator='=',
                alertThreshold='0',
                distributionList=testcasename,
                active=True)

        # Start batch
        batchrecord = batch.logbatch(testcasename, 'Batch start')

        # Start session
        event.logevent(indicatorlist[0].id, batchrecord.id, 'Session start')

        # Stop session
        sessionstopevent = event.logevent(indicatorlist[0].id, batchrecord.id, 'Session stop')

        # Get session
        with database.Function('Session') as function:
            sessionlist = function.read(indicatorId=indicatorlist[0].id, batchId=batchrecord.id)

        self.assertEqual(sessionlist[0].statusId, 2)
        self.assertEqual(sessionstopevent.eventTypeId, 2)
        self.assertEqual(sessionstopevent.sessionId, sessionlist[0].id)

    def test_logevent_error(self):
        """Test log event function with error event."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append(testcasename)

        # Create batch owner
        with database.Function('BatchOwner') as function:
            batchownerlist = function.create(name=testcasename)

        # Create data quality indicator
        with database.Function('Indicator') as function:
            indicatorlist = function.create(
                name=testcasename,
                description=testcasename,
                indicatorTypeId=1,
                batchOwnerId=batchownerlist[0].id,
                executionOrder=0,
                alertOperator='=',
                alertThreshold='0',
                distributionList=testcasename,
                active=True)

        # Start batch
        batchrecord = batch.logbatch(testcasename, 'Batch start')

        # Start session
        event.logevent(indicatorlist[0].id, batchrecord.id, 'Session start')

        # Error
        errorevent = event.logevent(indicatorlist[0].id, batchrecord.id, 'Error')

        # Get session
        with database.Function('Session') as function:
            sessionlist = function.read(indicatorId=indicatorlist[0].id, batchId=batchrecord.id)

        self.assertEqual(sessionlist[0].statusId, 3)
        self.assertEqual(errorevent.eventTypeId, 3)
        self.assertEqual(errorevent.sessionId, sessionlist[0].id)

    def test_logevent_dataset(self):
        """Test log event function with error event."""
        testcasename = test_utils.testcasename(self.testcaselist)
        self.testcaselist.append(testcasename)

        # Create batch owner
        with database.Function('BatchOwner') as function:
            batchownerlist = function.create(name=testcasename)

        # Create data quality indicator
        with database.Function('Indicator') as function:
            indicatorlist = function.create(
                name=testcasename,
                description=testcasename,
                indicatorTypeId=1,
                batchOwnerId=batchownerlist[0].id,
                executionOrder=0,
                alertOperator='=',
                alertThreshold='0',
                distributionList=testcasename,
                active=True)

        # Start batch
        batchrecord = batch.logbatch(testcasename, 'Batch start')

        # Start session
        event.logevent(indicatorlist[0].id, batchrecord.id, 'Session start')

        # Data set
        dataset = {'key': 'value'}
        datasetevent = event.logevent(indicatorlist[0].id, batchrecord.id, 'Data set', dataset)

        # Get session
        with database.Function('Session') as function:
            sessionlist = function.read(indicatorId=indicatorlist[0].id, batchId=batchrecord.id)

        self.assertEqual(sessionlist[0].statusId, 1)
        self.assertEqual(datasetevent.eventTypeId, 4)
        self.assertEqual(datasetevent.sessionId, sessionlist[0].id)
        self.assertEqual(datasetevent.content, dataset)

    @classmethod
    def tearDownClass(self):
        """Tear down function called when class is deconstructed."""
        for testcasename in self.testcaselist:
            # Delete indicator
            with database.Function('Indicator') as function:
                function.delete(name=testcasename)

            # Delete batch owner, batch, session, event
            with database.Function('BatchOwner') as function:
                function.delete(name=testcasename)

if __name__ == '__main__':
    # Test log event function in event module
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEventModule)
    unittest.TextTestRunner(verbosity=2).run(suite)

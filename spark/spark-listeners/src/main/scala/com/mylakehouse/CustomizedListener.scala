package com.mylakehouse

import com.mylakehouse.CustomizedListener.getApplicationSet
import org.apache.spark.scheduler.{SparkListener, SparkListenerApplicationEnd, SparkListenerApplicationStart, SparkListenerEvent, SparkListenerTaskEnd, SparkListenerTaskStart}
import org.apache.spark.sql.execution.ui.{SparkListenerSQLExecutionEnd, SparkListenerSQLExecutionStart}
import org.apache.spark.sql.util.QueryExecutionListener
import org.apache.spark.sql.execution.QueryExecution

import scala.collection.mutable
import scala.reflect.runtime.universe.{TermName, runtimeMirror, typeOf}

// this object contains all static variables and methods that are shared among all instances of the com.mylakehouse.CustomizedListener class
object CustomizedListener {

  // create a mutable HashSet to store all IDs of applications that are currently running
  private val applicationSet = mutable.Set.empty[String]

  // create a method to return an immutable deep copy of applicationSet
  def getApplicationSet: Set[String] = applicationSet.toSet

  // create a mutable HashMap to store all queries that are currently running
  private val runningQueryMap: mutable.HashMap[Long, mutable.HashMap[String, Any]] = mutable.HashMap.empty

  // create a method to return an immutable deep copy of runningQueryMap
  def getRunningQueryMap: Map[Long, Map[String, Any]] = {
    runningQueryMap.map { case (queryId, queryInfo) =>
      queryId -> queryInfo.toMap
    }.toMap
  }

  // create a mutable HashMap named endedQueryMap to store all detailed query info when a query ends
  // where key is the query id,
  // and value is another mutable hashmap that contains more detailed info about this query
  // (its application ID, start time, end time, duration, SQL context)
  private val endedQueryMap: mutable.HashMap[Long, mutable.HashMap[String, Any]] = mutable.HashMap.empty

  // create a method to return an immutable deep copy of endedQueryMap
  def getEndedQueryMap: Map[Long, Map[String, Any]] = {
    endedQueryMap.map { case (queryId, queryInfo) =>
      queryId -> queryInfo.toMap
    }.toMap
  }

}

class CustomizedListener extends SparkListener{
  private var curAppId = ""

  override def onApplicationStart(applicationStart: SparkListenerApplicationStart): Unit = {
    curAppId = applicationStart.appId.get
    CustomizedListener.applicationSet.add(curAppId)
    PushGateway.pushApplication(CustomizedListener.getApplicationSet)

    // print the HashSet after adding the ID of the application that has started
    println(s"Application started: ${getApplicationSet}")
  }

  override def onApplicationEnd(applicationEnd: SparkListenerApplicationEnd): Unit = {
    CustomizedListener.applicationSet.remove(curAppId)
    PushGateway.pushApplication(CustomizedListener.getApplicationSet)

    // print the HashSet after removing the ID of the application that has ended
    println(s"Application ended: ${getApplicationSet}")
  }

  // override the onOtherEvent method to capture SQL-query events
  override def onOtherEvent(event: SparkListenerEvent): Unit = event match {
    case e: SparkListenerSQLExecutionStart => onSQLExecutionStart(e)
    case e: SparkListenerSQLExecutionEnd => onSQLExecutionEnd(e)
  }


  // when a query starts, this method will capture its query info, store it to runningQueryMap and endedQueryMap,
  // and send it to the PushGateway
  private def onSQLExecutionStart(event: SparkListenerSQLExecutionStart): Unit = {
    // get query ID
    val queryId = event.executionId

    // get the application ID of the query
    val queryStartTime = event.time

    // add application ID to the runningQueryMap
    CustomizedListener.runningQueryMap += (queryId -> mutable.HashMap[String, Any]("Application Id" -> curAppId))

    // create a map that stores the query ID and its associated application ID and start time
    val queryInfoAtStart = mutable.HashMap[String, Any](
      "Application Id" -> curAppId,
      "Start Time" -> queryStartTime
    )

    CustomizedListener.endedQueryMap += (queryId -> queryInfoAtStart)

    //    PushGateway.pushQuery(CustomizedListener.getRunningQueryMap)

    // for testing purposes, print the query ID, application ID, and start time of the query
//    println(s"---------Query started: Query ID: $queryId, Application ID: $curAppId, Start Time: $queryStartTime")

    // for testing purpose, print all entries in runningQueryMap
//    CustomizedListener.runningQueryMap.foreach { case (key, value) =>
//      println(s"Key: $key, Value: $value")
//    }

    // for testing purpose, print getRunningQueryMap
    println(CustomizedListener.getRunningQueryMap)
  }

  // when a query ends, this method will capture its query info, add it to endedQueryMap,
  // remove it from the runningQueryMap, push both maps to the PushGateway, and remove it from endedQueryMap
  private def onSQLExecutionEnd(event: SparkListenerSQLExecutionEnd): Unit = {
    Thread.sleep(5000)

    // get query ID
    val queryId = event.executionId

    // get the end time of the query
    val queryEndTime = event.time

    // get the duration of the query
    val queryStartTime = CustomizedListener.endedQueryMap(queryId)("Start Time").asInstanceOf[Long]
    val duration = queryEndTime - queryStartTime

    // use reflection to get the private field qe from the event
    // since we can get the query context from qe
    val mirror = runtimeMirror(getClass.getClassLoader)
    val instanceMirror = mirror.reflect(event)
    val qeField = typeOf[SparkListenerSQLExecutionEnd].decl(TermName("qe")).asTerm
    val value = instanceMirror.reflectField(qeField).get.asInstanceOf[QueryExecution]

    // get the query context
    val queryContext = value.logical.origin.sqlText.getOrElse(value.logical.toString())

    // remove the query ID from the runningQueryMap
    CustomizedListener.runningQueryMap.remove(queryId)

    //    PushGateway.pushQuery(CustomizedListener.getRunningQueryMap)

    // Append queryEndTime, duration, and queryContext to the endedQueryMap
    CustomizedListener.endedQueryMap.get(queryId) match {
      case Some(queryInfo) =>
        queryInfo += ("End Time" -> queryEndTime)
        queryInfo += ("Duration(ms)" -> duration)
        queryInfo += ("Query Context" -> queryContext)
      case None =>
        // Handle the case when the queryId is not found in the queryMap
        println(s"Query ID $queryId not found in the queryMap")
    }

    //    PushGateway.pushQuery(CustomizedListener.getEndedQueryMap)


    // for testing purpose, print the query ID, end time, duration, and query context of the query
//    println(s"----------Query ended: Query ID: $queryId, End Time: $queryEndTime, Duration: $duration, Query Context: $queryContext")

    // for testing purpose, print all entries in queryMap
//    CustomizedListener.endedQueryMap.foreach { case (key, value) =>
//      println(s"Key: $key, Value: $value")
//    }

    CustomizedListener.endedQueryMap.remove(queryId)

    // for testing purpose, print getEndedQueryMap
    println(CustomizedListener.getEndedQueryMap)
  }
}
package com.mylakehouse

import com.mylakehouse.CustomizedListener.getApplicationSet
import org.apache.spark.scheduler.{SparkListener, SparkListenerApplicationEnd, SparkListenerApplicationStart, SparkListenerEvent}
import org.apache.spark.sql.execution.ui.{SparkListenerSQLExecutionEnd, SparkListenerSQLExecutionStart}

import scala.collection.mutable

// this object contains all static variables and methods that are shared among all instances of the com.mylakehouse.CustomizedListener class
object CustomizedListener {
  // create a mutable HashSet to store all IDs of applications that are currently running
  private val applicationSet = mutable.Set.empty[String]

  // create a mutable HashMap to store all IDs of queries that are currently running and the their associated application IDs
  private val queryMap = mutable.HashMap.empty[Long, String]

  // create a method to return an immutable deep copy of applicationSet
  def getApplicationSet: Set[String] = applicationSet.toSet

  // create a method to return an immutable deep copy of queryMap
  def getQueryMap: Map[Long, String] = queryMap.toMap
}

class CustomizedListener extends SparkListener {
  private var curAppId = ""

  override def onApplicationStart(applicationStart: SparkListenerApplicationStart): Unit = {
    curAppId = applicationStart.appId.get
    CustomizedListener.applicationSet.add(curAppId)
    PushGateway.push(CustomizedListener.getApplicationSet)

    // print the HashSet after adding the ID of the application that has started
    println(s"Application started: ${getApplicationSet}")
  }

  override def onApplicationEnd(applicationEnd: SparkListenerApplicationEnd): Unit = {
    CustomizedListener.applicationSet.remove(curAppId)
    PushGateway.push(CustomizedListener.getApplicationSet)

    // print the HashSet after removing the ID of the application that has ended
    println(s"Application ended: ${getApplicationSet}")
  }

  // override the onOtherEvent method to capture SQL-query events
  override def onOtherEvent(event: SparkListenerEvent): Unit = event match {
    case e: SparkListenerSQLExecutionStart => onExecutionStart(e)
    case e: SparkListenerSQLExecutionEnd => onExecutionEnd(e)
  }

  // when a SQL query starts, create a method to capture its query Id and associate application Id
  // and add it to the queryMap which stores all currently running queries
  private def onExecutionStart(event: SparkListenerSQLExecutionStart): Unit = {
    val queryId = event.executionId
    CustomizedListener.queryMap.put(queryId, curAppId)

    println(s"---------Query started: Query ID: $queryId, Application ID: $curAppId")

    // print all entries in HashMap after adding the query that has started
    println(s"HashMap after adding the query: ${CustomizedListener.getQueryMap}")
  }

  // when a SQL query ends, remove it from the queryMap
  private def onExecutionEnd(event: SparkListenerSQLExecutionEnd): Unit = {
    val queryId = event.executionId
    CustomizedListener.queryMap.remove(queryId)

    println(s"----------Query ended: Query ID: $queryId")

    // print all entries in HashMap after removing the query that has ended
    println(s"HashMap after removing the query: ${CustomizedListener.getQueryMap}")
  }

}
package listeners

import listeners.CustomizedListener.getApplicationSet
import org.apache.spark.scheduler.{SparkListener, SparkListenerApplicationEnd, SparkListenerApplicationStart}

import scala.collection.mutable

// this object contains all static variables and methods that are shared among all instances of the CustomizedListener class
object CustomizedListener {
  // create a mutable HashSet to store the ID of applications that are currently running
  private val applicationSet = mutable.Set.empty[String]

  // create a method to return an immutable deep copy of applicationSet
  def getApplicationSet: Set[String] = applicationSet.toSet
}

class CustomizedListener extends SparkListener {
  private var curAppId = ""

  override def onApplicationStart(applicationStart: SparkListenerApplicationStart): Unit = {
    curAppId = applicationStart.appId.get
    CustomizedListener.applicationSet.add(curAppId)

    // print the HashSet after adding the ID of the application that has started
    println(s"Application started: ${getApplicationSet}")
  }

  override def onApplicationEnd(applicationEnd: SparkListenerApplicationEnd): Unit = {
    // print the HashSet before removing the ID of the application that has ended
    println(s"Application ended (before removing the application): ${getApplicationSet}")

    CustomizedListener.applicationSet.remove(curAppId)

    // print the HashSet after removing the ID of the application that has ended
    println(s"Application ended (before removing the application): ${getApplicationSet}")
  }

}
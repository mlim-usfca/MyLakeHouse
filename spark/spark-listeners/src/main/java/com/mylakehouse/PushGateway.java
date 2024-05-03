package com.mylakehouse;

import io.prometheus.client.Gauge;
import scala.Long;
import scala.collection.Iterator;
import scala.collection.immutable.Set;
import io.prometheus.client.CollectorRegistry;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class PushGateway {
    public static void pushApplication(Set<String> applicationSet) {
        System.out.println("Got set : " + applicationSet);

        // Create a CollectorRegistry
        CollectorRegistry registry = new CollectorRegistry();

        if (applicationSet.size() == 0) {
            // Create an empty Gauge metric
            Gauge gauge = Gauge.build()
                    .name("app_metric")
                    .help("An empty gauge")
                    .register(registry);

            IndexGenerator.setAppMap(new HashMap<>());
            IndexGenerator.resetAppBool();

        } else {
            // System.out.println("else Got set : " + applicationSet);
            try {
                // Create a Gauge metric
                Gauge gauge = Gauge.build()
                        .name("app_metric")
                        .help("metric of app name")
                        .labelNames("app_name")
                        .register(registry);

                // add another map to record which query is not running anymore
                Map<String, Integer> appMapTemp = new HashMap<>();

                // Set the value of the Gauge metric
                Iterator<String> iterator = applicationSet.iterator();
                while (iterator.hasNext()) {
                    String element = iterator.next();
                    int idx = IndexGenerator.getAppIdx(element);
                    gauge.labels(element).set(idx + 1);

                    appMapTemp.put(element, idx);
                    IndexGenerator.appMapRemove(element); // the rest will be queries not running anymore
                }

                for (Map.Entry<String, Integer> entry : IndexGenerator.getAppMap().entrySet()) {
                    int id = entry.getValue();
                    IndexGenerator.removeAppIdx(id);
                }
                IndexGenerator.setAppMap(appMapTemp);

            } catch (Exception e) {
                System.out.println("Failed to build a gauge in pushApplication()");
            }
        }

        io.prometheus.client.exporter.PushGateway pushGateway = new io.prometheus.client.exporter.PushGateway("pushgateway:9091");

        try {
            pushGateway.pushAdd(registry, "application_name");
            System.out.println("Successfully pushed application name with set + " + applicationSet);
        } catch (IOException e) {
            System.out.println("Failed to push application. Error message: " + e.getMessage());
        }
    }

    public static void pushQuery(Map<scala.Long, Map<String, Object>> appQueryMap) {
        System.out.println("pushgateway + appQueryMap : " + appQueryMap);

        // Create a CollectorRegistry
        CollectorRegistry registry = new CollectorRegistry();

        if (appQueryMap.size() == 0) {
            System.out.println("query Application Map size is 0");
            // Create an empty Gauge metric
            Gauge gauge = Gauge.build()
                    .name("query_app_metric")
                    .help("An empty gauge")
                    .register(registry);

            IndexGenerator.setAppQueryMap(new HashMap<>());
            IndexGenerator.resetAppQueryBool();
        } else {
            try {
                // Create a Gauge metric
                Gauge gauge = Gauge.build()
                        .name("query_app_metric")
                        .help("metric of query ID with corresponding application name")
                        .labelNames("query", "application")
                        .register(registry);

                // add another map to record which query is not running anymore
                Map<String, Integer> queryMapTemp = new HashMap<>();

                // Set the value of the Gauge metric
                for (Map.Entry<scala.Long, Map<String, Object>> entry : appQueryMap.entrySet()) {
                    String queryID = String.valueOf(entry.getKey());

                    String appID = "";
                    for (Map.Entry<String, Object> labels : entry.getValue().entrySet()) {
                        if (labels.getKey().equals("Application Name")) {
                            appID = labels.getValue().toString();
                        }
                    }

                    int idx = IndexGenerator.getQueryIdx(queryID);
                    gauge.labels(queryID, appID).set(idx + 1);
                    queryMapTemp.put(queryID, idx);
                    IndexGenerator.appQueryMapRemove(queryID); // the rest will be queries not running anymore
                }

                for (Map.Entry<String, Integer> entry : IndexGenerator.getAppQueryMap().entrySet()) {
                    int id = entry.getValue();
                    IndexGenerator.removeQueryIdx(id);
                }

                IndexGenerator.setAppQueryMap(queryMapTemp);
            } catch (Exception e) {
                System.out.println("Failed to build a gauge in pushQuery()");
            }
        }

        // Push metrics to the Pushgateway
        io.prometheus.client.exporter.PushGateway pushGateway = new io.prometheus.client.exporter.PushGateway("pushgateway:9091");

        try {
            pushGateway.pushAdd(registry, "query_Application_ID");
            System.out.println("Successfully pushed query_Application_ID with map" + appQueryMap);
        } catch (IOException e) {
            System.out.println("Failed to push query-application. Error message: " + e.getMessage());
        }
    }

    public static void pushSQLQuery(Map<scala.Long, Map<String, Object>> sqlDurationMap) {
        System.out.println("pushgateway + pushSQLQuery + appQueryMap : " + sqlDurationMap);

        for (Map.Entry<Long, Map<String, Object>> entry : sqlDurationMap.entrySet()) {
            System.out.println(entry.getKey());
            for (Map.Entry<String, Object> labels : entry.getValue().entrySet()) {
                System.out.println(labels.getKey());
                System.out.println(labels.getValue());
            }
        }

        // Create a CollectorRegistry
        CollectorRegistry registry = new CollectorRegistry();

        if (sqlDurationMap.size() == 0) {
            // Create an empty Gauge metric
            Gauge gauge = Gauge.build()
                    .name("sql_query_duration")
                    .help("An empty gauge")
                    .register(registry);
        } else {
            // Create a Gauge metric
            try {
                Gauge gauge = Gauge.build()
                        .name("sql_query_duration")
                        .help("metric of query ID with corresponding application name")
                        .labelNames("app_name", "query_ID", "SQL_context", "duration_unit")
                        .register(registry);

                // Set the value of the Gauge metric
                for (Map.Entry<Long, Map<String, Object>> entry : sqlDurationMap.entrySet()) {
                    String queryID = String.valueOf(entry.getKey());
                    String appID = "";
                    double duration = 0;
                    String SQLquery = "";

                    for (Map.Entry<String, Object> labels : entry.getValue().entrySet()) {
                        switch (labels.getKey()) {
                            case "Application Name":
                                appID = labels.getValue().toString();
                                break;
                            case "Duration(ms)":
                                duration = Double.parseDouble(labels.getValue().toString()) / 1000;
                                break;
                            case "Query Context":
                                SQLquery = labels.getValue().toString();
                                SQLquery = SQLquery.replace("\n", "");
                                break;
                        }
                    }

                    System.out.println(SQLquery);

                    gauge.labels(appID, queryID, SQLquery, "second").set(duration);
                }
            } catch (Exception e) {
                System.out.println("Failed to build a gauge in pushSQLQuery()");
            }
        }

        // Push metrics to the Pushgateway
        io.prometheus.client.exporter.PushGateway pushGateway = new io.prometheus.client.exporter.PushGateway("pushgateway:9091");

        try {
            pushGateway.pushAdd(registry, "sql_duration");
            System.out.println("Successfully pushed sql_duration with map" + sqlDurationMap);
        } catch (IOException e) {
            System.out.println("Failed to push query-application. Error message: " + e.getMessage());
        }
    }
}

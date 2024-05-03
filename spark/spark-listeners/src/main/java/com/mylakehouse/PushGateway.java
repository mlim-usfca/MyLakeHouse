package com.mylakehouse;

import io.prometheus.client.Gauge;
import scala.Long;
import scala.collection.Iterator;
import scala.collection.JavaConverters;
import scala.collection.immutable.Set;
import io.prometheus.client.CollectorRegistry;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class PushGateway {
    private static boolean[] appIDbool = new boolean[10]; // False as empty, True as occupied
    private static Map<String, Integer> appMap = new HashMap<>();
    private static boolean[] queryIDbool = new boolean[10]; // False as empty, True as occupied
    private static Map<String, Integer> queryMap = new HashMap<>();

    private static int getAppIdx(String appId) {
        // If the query has been still running since last time we pushed the metric
        if (appMap.containsKey(appId)) {
            return appMap.get(appId);
        }

        // If the query is a new one, assign an unused index to it
        for (int i = 0; i < appIDbool.length; i++) {
            if (!appIDbool[i]) {
                appIDbool[i] = true;
                return i;
            }
        }

        // if it is at capacity, extend the boolean array and assign the index of n + 1 to it
        boolean[] copy = new boolean[appIDbool.length * 2];
        for (int i = 0; i < appIDbool.length + 1; i++) {
            copy[i] = true;
        }

        System.out.println("boolean array for application id extended, previous: " + appIDbool.length + " new: " + copy.length);

        int ret = appIDbool.length + 1;
        appIDbool = copy;

        return ret;
    }

    private static void removeAppIdx(int idx) {
        appIDbool[idx] = false;

        if (appIDbool.length <= 10) {
            return;
        }

        // if the second half of it is empty then shrink the array
        for (int i = appIDbool.length - 1; i > appIDbool.length / 2; i--) {
            if (appIDbool[i]) {
                return;
            }
        }

        boolean[] copy = new boolean[appIDbool.length / 2];
        System.arraycopy(appIDbool, 0, copy, 0, copy.length);

        System.out.println("boolean array for application id shrank, previous: " + appIDbool.length + " new: " + copy.length);
        appIDbool = copy;
    }

    private static int getQueryIdx(String appId) {
        // If the query has been still running since last time we pushed the metric
        if (queryMap.containsKey(appId)) {
            return queryMap.get(appId);
        }

        // If the query is a new one, assign an unused index to it
        for (int i = 0; i < queryIDbool.length; i++) {
            if (!queryIDbool[i]) {
                queryIDbool[i] = true;
                return i;
            }
        }

        // if it is at capacity, extend the boolean array and assign the index of n + 1 to it
        boolean[] copy = new boolean[queryIDbool.length * 2];
        for (int i = 0; i < queryIDbool.length + 1; i++) {
            copy[i] = true;
        }

        System.out.println("boolean array for application id extended, previous: " + queryIDbool.length + " new: " + copy.length);

        int ret = queryIDbool.length + 1;
        queryIDbool = copy;

        return ret;
    }

    private static void removeQueryIdx(int idx) {
        queryIDbool[idx] = false;

        if (queryIDbool.length <= 10) {
            return;
        }

        // if the second half of it is empty then shrink the array
        for (int i = queryIDbool.length - 1; i > queryIDbool.length / 2; i--) {
            if (queryIDbool[i]) {
                return;
            }
        }

        boolean[] copy = new boolean[queryIDbool.length / 2];
        System.arraycopy(queryIDbool, 0, copy, 0, copy.length);

        System.out.println("boolean array for query id shrank, previous: " + queryIDbool.length + " new: " + copy.length);
        queryIDbool = copy;
    }

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
            appMap = new HashMap<>();
            appIDbool = new boolean[10];
        } else {
            try {
                // Create a Gauge metric
                Gauge gauge = Gauge.build()
                        .name("app_metric")
                        .help("metric of app ID")
                        .labelNames("app_ID")
                        .register(registry);

                // add another map to record which query is not running anymore
                Map<String, Integer> appMapTemp = new HashMap<>();

                // Set the value of the Gauge metric
                Iterator<String> iterator = applicationSet.iterator();
                while (iterator.hasNext()) {
                    String element = iterator.next();
                    int idx = getAppIdx(element);
                    gauge.labels(element).set(idx + 1);

                    appMapTemp.put(element, idx);
                    appMap.remove(element); // the rest will be queries not running anymore
                }

                for (Map.Entry<String, Integer> entry: appMap.entrySet()) {
                    int id = entry.getValue();
                    removeAppIdx(id);
                }
                appMap = appMapTemp;
            } catch (Exception e) {
                System.out.println("Failed to build a gauge in pushApplication()");
            }
        }

        io.prometheus.client.exporter.PushGateway pushGateway = new io.prometheus.client.exporter.PushGateway("pushgateway:9091");

        try {
            pushGateway.pushAdd(registry, "application_ID");
            System.out.println("Successfully pushed application ID with set + " + applicationSet);
        } catch (IOException e) {
            System.out.println("Failed to push application. Error message: " + e.getMessage());
        }
    }

    public static void pushQuery(Map<scala.Long, Map<String, Object>> appQueryMap) {
        System.out.println("pushgateway + queryAppMap : " + appQueryMap);

        // Create a CollectorRegistry
        CollectorRegistry registry = new CollectorRegistry();

        if (appQueryMap.size() == 0) {
            // Create an empty Gauge metric
            Gauge gauge = Gauge.build()
                    .name("query_app_metric")
                    .help("An empty gauge")
                    .register(registry);

            queryMap = new HashMap<>();
            queryIDbool = new boolean[10];
        } else {
            try {
                // Create a Gauge metric
                Gauge gauge = Gauge.build()
                        .name("query_app_metric")
                        .help("metric of query ID with corresponding application ID")
                        .labelNames("query", "application")
                        .register(registry);

                // add another map to record which query is not running anymore
                Map<String, Integer> queryMapTemp = new HashMap<>();

                // Set the value of the Gauge metric
                for (Map.Entry<scala.Long, Map<String, Object>> entry : appQueryMap.entrySet()) {
                    String queryID = String.valueOf(entry.getKey());

                    String appID = "";
                    for (Map.Entry<String, Object> labels : entry.getValue().entrySet()) {
                        if (labels.getKey().equals("Application Id")) {
                            appID = labels.getValue().toString();
                        }
                    }

                    int idx = getQueryIdx(queryID);
                    gauge.labels(queryID, appID).set(idx + 1);

                    queryMapTemp.put(queryID, idx);
                    queryMap.remove(queryID); // the rest will be queries not running anymore
                }

                for (Map.Entry<String, Integer> entry : IndexGenerator.getAppQueryMap().entrySet()) {
                    int id = entry.getValue();
                    removeQueryIdx(id);
                }
                queryMap = queryMapTemp;
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
}

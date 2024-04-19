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
        // Create a CollectorRegistry
        CollectorRegistry registry = new CollectorRegistry();

        if (applicationSet.size() == 0) {
            // Create an empty Gauge metric
            Gauge gauge = Gauge.build()
                    .name("query_metric")
                    .help("An empty gauge")
                    .register(registry);
            appMap = new HashMap<>();
            appIDbool = new boolean[10];
        } else {
            // Create a Gauge metric
            Gauge gauge = Gauge.build()
                    .name("query_metric")
                    .help("metric of query ID")
                    .labelNames("query ID")
                    .register(registry);

            // add another map to record which query is not running anymore
            Map<String, Integer> appMapTemp = new HashMap<>();

            // Set the value of the Gauge metric
            Iterator<String> iterator = applicationSet.iterator();
            while (iterator.hasNext()) {
                String element = iterator.next();
                int idx = getAppIdx(element);
                gauge.labels(element).set(idx);

                appMapTemp.put(element, idx);
                appMap.remove(element); // the rest will be queries not running anymore
            }

            for (Map.Entry<String, Integer> entry: appMap.entrySet()) {
                int id = entry.getValue();
                removeAppIdx(id);
            }
            appMap = appMapTemp;
        }

        // Push metrics to the Pushgateway
        io.prometheus.client.exporter.PushGateway pushGateway = new io.prometheus.client.exporter.PushGateway("pushgateway:9091");

        try {
            pushGateway.pushAdd(registry, "queryID");
            System.out.println("Successfully pushed queryID with set + " + applicationSet);
        } catch (IOException e) {
            System.out.println("Error message: " + e.getMessage());
        }
    }

    public static void pushQuery(scala.collection.immutable.Map<scala.Long, String> scalaMap) {
        System.out.println("pushgateway + queryAppMap : " + scalaMap);
        Map<Long, String> queryAppMap = JavaConverters.mapAsJavaMap(scalaMap);

        // Create a CollectorRegistry
        CollectorRegistry registry = new CollectorRegistry();

        if (scalaMap.size() == 0) {
            // Create an empty Gauge metric
            Gauge gauge = Gauge.build()
                    .name("query_app_metric")
                    .help("An empty gauge")
                    .register(registry);
        } else {
            // Create a Gauge metric
            Gauge gauge = Gauge.build()
                    .name("query_app_metric")
                    .help("metric of query ID with corresponding application ID")
                    .labelNames("query", "application")
                    .register(registry);

            // add another map to record which query is not running anymore
            Map<String, Integer> queryMapTemp = new HashMap<>();

            // Set the value of the Gauge metric
            for (Map.Entry<scala.Long, String> entry : queryAppMap.entrySet()) {
                String query = String.valueOf(entry.getKey());
                String app = entry.getValue();
                int idx = getQueryIdx(query);
                gauge.labels(query, app).set(idx);

                queryMapTemp.put(query, idx);
                queryMap.remove(query); // the rest will be queries not running anymore
            }

            for (Map.Entry<String, Integer> entry: queryMap.entrySet()) {
                int id = entry.getValue();
                removeQueryIdx(id);
            }
            queryMap = queryMapTemp;
        }
        
        // Push metrics to the Pushgateway
        io.prometheus.client.exporter.PushGateway pushGateway = new io.prometheus.client.exporter.PushGateway("pushgateway:9091");

        try {
            pushGateway.pushAdd(registry, "query_Application_ID");
            System.out.println("Successfully pushed query_Application_ID with map" + queryAppMap);
        } catch (IOException e) {
            System.out.println("Error message: " + e.getMessage());
        }
    }
}

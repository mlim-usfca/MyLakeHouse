package com.mylakehouse;

import io.prometheus.client.Gauge;
import scala.Long;
import scala.collection.Iterator;
import scala.collection.JavaConverters;
import scala.collection.immutable.Set;
import io.prometheus.client.CollectorRegistry;

import java.io.IOException;
import java.util.Map;

public class PushGateway {
    public static void pushApplication(Set<String> applicationSet) {
        // Create a CollectorRegistry
        CollectorRegistry registry = new CollectorRegistry();

        if (applicationSet.size() == 0) {
            // Create an empty Gauge metric
            Gauge gauge = Gauge.build()
                    .name("query_metric")
                    .help("An empty gauge")
                    .register(registry);
        } else {
            // Create a Gauge metric
            Gauge gauge = Gauge.build()
                    .name("query_metric")
                    .help("metric of query ID")
                    .labelNames("query ID")
                    .register(registry);

            // Set the value of the Gauge metric
            Iterator<String> iterator = applicationSet.iterator();
            while (iterator.hasNext()) {
                String element = iterator.next();
                gauge.labels(element).set(1);
            }
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

            // Set the value of the Gauge metric
            for (Map.Entry<scala.Long, String> entry : queryAppMap.entrySet()) {
                String query = String.valueOf(entry.getKey());
                String app = entry.getValue();
                gauge.labels(query, app).set(1);
            }
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

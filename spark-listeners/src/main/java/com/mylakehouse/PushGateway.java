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
        System.out.println("pushgateway + " + applicationSet);

        // Create a CollectorRegistry
        CollectorRegistry registry = new CollectorRegistry();

        // Create a Gauge metric
        Gauge gauge = Gauge.build()
                .name("my_custom_metric")
                .help("Description of my custom metric")
                .labelNames("element")
                .register(registry);

        // Set the value of the Gauge metric
        Iterator<String> iterator = applicationSet.iterator();
        while (iterator.hasNext()) {
            String element = iterator.next();
            gauge.labels(element).set(1);
        }

        System.out.println(registry);
        // Push metrics to the Pushgateway
        io.prometheus.client.exporter.PushGateway pushGateway = new io.prometheus.client.exporter.PushGateway("127.0.0.1:9091");

        try {
            pushGateway.pushAdd(registry, "my_job");
            System.out.println("Successfully pushed my_job");
        } catch (IOException e) {
            System.out.println("Error message: " + e.getMessage());
        }
    }

    public static void pushQuery(scala.collection.immutable.Map<scala.Long, String> scalaMap) {
        System.out.println("pushgateway + queryAppMap : " + scalaMap);
        Map<Long, String> queryAppMap = JavaConverters.mapAsJavaMap(scalaMap);

        // Create a CollectorRegistry
        CollectorRegistry registry = new CollectorRegistry();

        // Create a Gauge metric
        Gauge gauge = Gauge.build()
                .name("my_query_app_metric")
                .help("Description of my custom metric")
                .labelNames("query", "application")
                .register(registry);

        // Set the value of the Gauge metric
        for (Map.Entry<scala.Long, String> entry : queryAppMap.entrySet()) {
            String query = String.valueOf(entry.getKey());
            String app = entry.getValue();
            System.out.println("pushgateway app: " + app);
            gauge.labels(query, app).set(1);
        }

        System.out.println(registry);
        // Push metrics to the Pushgateway
        io.prometheus.client.exporter.PushGateway pushGateway = new io.prometheus.client.exporter.PushGateway("127.0.0.1:9091");

        try {
            pushGateway.pushAdd(registry, "my_query_app_job");
            System.out.println("Successfully pushed my_query_app_job");
        } catch (IOException e) {
            System.out.println("Error message: " + e.getMessage());
        }
    }
}

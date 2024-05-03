package com.mylakehouse;

import java.util.HashMap;
import java.util.Map;

public class IndexGenerator {
    private static boolean[] appIDbool = new boolean[10]; // False as empty, True as occupied
    private static Map<String, Integer> appMap = new HashMap<>();
    private static boolean[] queryIDbool = new boolean[10]; // False as empty, True as occupied
    private static Map<String, Integer> queryMap = new HashMap<>();

    public static void setAppMap(Map<String, Integer> map) {
        appMap = map;
    }

    public static void setAppQueryMap(Map<String, Integer> map) {
        queryMap = map;
    }

    public static void resetAppBool() {
        appIDbool = new boolean[10];
    }

    public static void resetAppQueryBool() {
        queryIDbool = new boolean[10];
    }

    public static void appMapRemove(String index) {
        appMap.remove(index);
    }

    public static void appQueryMapRemove(String index) {
        queryMap.remove(index);
    }

    public static Map<String, Integer> getAppMap() {
        return appMap;
    }

    public static Map<String, Integer> getAppQueryMap() {
        return queryMap;
    }

    public static int getAppIdx(String appId) {
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

    public static void removeAppIdx(int idx) {
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

    public static int getQueryIdx(String appId) {
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

    public static void removeQueryIdx(int idx) {
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
}

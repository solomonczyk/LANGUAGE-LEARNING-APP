import { Stack } from "expo-router";
import { StatusBar } from "expo-status-bar";
import { SafeAreaProvider } from "react-native-safe-area-context";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Text, View } from "react-native";

const queryClient = new QueryClient();

export default function RootLayout() {
  return (
    <QueryClientProvider client={queryClient}>
      <SafeAreaProvider>
        <StatusBar style="dark" />
        <Stack
          screenOptions={{
            headerShown: false,
            animation: "slide_from_right",
          }}
        >
          <Stack.Screen
            name="onboarding"
            options={{ headerShown: false, gestureEnabled: false }}
          />
          <Stack.Screen
            name="diagnostic"
            options={{ headerShown: false }}
          />
          <Stack.Screen
            name="learning-contract"
            options={{ headerShown: false }}
          />
          <Stack.Screen
            name="home"
            options={{ headerShown: false }}
          />
          <Stack.Screen
            name="lesson/[id]"
            options={{ headerShown: false }}
          />
          <Stack.Screen
            name="lesson-session/[id]"
            options={{ headerShown: false }}
          />
          <Stack.Screen
            name="result/[id]"
            options={{ headerShown: false }}
          />
        </Stack>
      </SafeAreaProvider>
    </QueryClientProvider>
  );
}

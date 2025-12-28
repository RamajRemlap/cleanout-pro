/**
 * CleanoutPro Mobile App
 * AI-powered junk removal estimates
 */

import React, { useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { StatusBar } from 'react-native';
import { GestureHandlerRootView } from 'react-native-gesture-handler';

// Screens
import { JobListScreen } from './src/screens/JobListScreen';
import { RoomListScreen } from './src/screens/RoomListScreen';
import { CaptureScreen } from './src/screens/CaptureScreen';
import { RoomDetailScreen } from './src/screens/RoomDetailScreen';

// Services
import syncService from './src/services/sync';
import { useAppStore } from './src/store';
import apiService from './src/services/api';

const Stack = createNativeStackNavigator();

export default function App() {
  const { setOffline, setPendingSyncCount } = useAppStore();

  useEffect(() => {
    // Initialize sync service
    syncService.init();

    // Check backend connectivity on mount
    checkConnectivity();

    // Set up periodic connectivity checks (every 30s)
    const interval = setInterval(checkConnectivity, 30000);

    return () => clearInterval(interval);
  }, []);

  const checkConnectivity = async () => {
    const isHealthy = await apiService.healthCheck();
    setOffline(!isHealthy);

    if (isHealthy) {
      // Try to sync pending operations
      const result = await syncService.processQueue();
      setPendingSyncCount(syncService.getPendingCount());

      if (result.success > 0) {
        console.log(`Auto-synced ${result.success} operations`);
      }
    } else {
      setPendingSyncCount(syncService.getPendingCount());
    }
  };

  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <StatusBar barStyle="dark-content" />
      <NavigationContainer>
        <Stack.Navigator
          initialRouteName="JobList"
          screenOptions={{
            headerStyle: {
              backgroundColor: '#fff',
            },
            headerTintColor: '#007AFF',
            headerTitleStyle: {
              fontWeight: 'bold',
            },
          }}>
          <Stack.Screen
            name="JobList"
            component={JobListScreen}
            options={{ title: 'CleanoutPro' }}
          />
          <Stack.Screen
            name="RoomList"
            component={RoomListScreen}
            options={{ title: 'Rooms' }}
          />
          <Stack.Screen
            name="Capture"
            component={CaptureScreen}
            options={{
              title: 'Capture Room',
              headerShown: false,
            }}
          />
          <Stack.Screen
            name="RoomDetail"
            component={RoomDetailScreen}
            options={{ title: 'Room Details' }}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </GestureHandlerRootView>
  );
}

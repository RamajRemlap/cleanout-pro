/**
 * Capture Screen
 * Wrapper for camera capture with upload logic
 */

import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
  ActivityIndicator,
  Image,
} from 'react-native';
import { CameraCapture } from '../components/CameraCapture';
import { useAppStore } from '../store';
import apiService from '../services/api';
import syncService from '../services/sync';

interface Props {
  navigation: any;
  route: any;
}

export const CaptureScreen: React.FC<Props> = ({ navigation, route }) => {
  const { jobId, roomNumber } = route.params;
  const [capturedUri, setCapturedUri] = useState<string | null>(null);
  const [roomName, setRoomName] = useState('');
  const [uploading, setUploading] = useState(false);
  const { addRoom, isOffline } = useAppStore();

  const handleCapture = (uri: string) => {
    setCapturedUri(uri);
  };

  const handleRetake = () => {
    setCapturedUri(null);
  };

  const handleUpload = async () => {
    if (!capturedUri || !roomName.trim()) {
      Alert.alert('Error', 'Please enter a room name');
      return;
    }

    setUploading(true);

    try {
      if (isOffline) {
        // Store locally for offline sync
        await syncService.addToQueue('create', 'room', '', {
          job_id: jobId,
          room_name: roomName,
          room_number: roomNumber,
          image_uri: capturedUri,
        });

        Alert.alert(
          'Offline Mode',
          'Room saved locally. Will sync when online.',
          [
            {
              text: 'OK',
              onPress: () => navigation.goBack(),
            },
          ]
        );
      } else {
        // Upload to backend
        const room = await apiService.uploadRoom(
          jobId,
          roomName,
          roomNumber,
          capturedUri
        );

        addRoom(room);

        Alert.alert(
          'Success',
          `Room "${roomName}" uploaded and analyzed!\n\n` +
            `Size: ${room.final_size_class}\n` +
            `Workload: ${room.final_workload_class}\n` +
            `Estimate: $${room.estimated_cost.toFixed(2)}\n` +
            `Confidence: ${((room.ai_confidence || 0) * 100).toFixed(0)}%`,
          [
            {
              text: 'Add Another Room',
              onPress: () => {
                setCapturedUri(null);
                setRoomName('');
              },
            },
            {
              text: 'View Details',
              onPress: () => {
                navigation.navigate('RoomDetail', { room });
              },
            },
            {
              text: 'Done',
              onPress: () => navigation.goBack(),
            },
          ]
        );
      }
    } catch (error: any) {
      console.error('Upload failed:', error);
      Alert.alert(
        'Upload Failed',
        error.response?.data?.detail || error.message || 'Unknown error',
        [
          {
            text: 'Save Offline',
            onPress: async () => {
              await syncService.addToQueue('create', 'room', '', {
                job_id: jobId,
                room_name: roomName,
                room_number: roomNumber,
                image_uri: capturedUri,
              });
              navigation.goBack();
            },
          },
          { text: 'Cancel', style: 'cancel' },
        ]
      );
    } finally {
      setUploading(false);
    }
  };

  if (!capturedUri) {
    return (
      <CameraCapture
        onCapture={handleCapture}
        onCancel={() => navigation.goBack()}
      />
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.preview}>
        <Image source={{ uri: capturedUri }} style={styles.previewImage} />
      </View>

      <View style={styles.form}>
        <Text style={styles.label}>Room Name</Text>
        <TextInput
          style={styles.input}
          placeholder="e.g., Master Bedroom, Garage, Basement"
          value={roomName}
          onChangeText={setRoomName}
          autoFocus
          autoCapitalize="words"
        />

        <Text style={styles.hint}>
          Room #{roomNumber} - AI will analyze the photo to estimate size and workload
        </Text>

        <View style={styles.buttons}>
          <TouchableOpacity
            style={styles.retakeButton}
            onPress={handleRetake}
            disabled={uploading}>
            <Text style={styles.retakeButtonText}>Retake</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.uploadButton, uploading && styles.uploadButtonDisabled]}
            onPress={handleUpload}
            disabled={uploading}>
            {uploading ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <Text style={styles.uploadButtonText}>
                {isOffline ? 'Save Offline' : 'Upload & Analyze'}
              </Text>
            )}
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  preview: {
    flex: 1,
    backgroundColor: '#000',
  },
  previewImage: {
    width: '100%',
    height: '100%',
    resizeMode: 'contain',
  },
  form: {
    backgroundColor: '#fff',
    padding: 20,
    borderTopLeftRadius: 24,
    borderTopRightRadius: 24,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: -4 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 10,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 8,
    color: '#333',
  },
  input: {
    backgroundColor: '#F5F5F5',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderRadius: 8,
    fontSize: 16,
    marginBottom: 12,
  },
  hint: {
    fontSize: 14,
    color: '#666',
    marginBottom: 20,
  },
  buttons: {
    flexDirection: 'row',
    gap: 12,
  },
  retakeButton: {
    flex: 1,
    backgroundColor: '#E5E5E5',
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  retakeButtonText: {
    color: '#333',
    fontSize: 16,
    fontWeight: '600',
  },
  uploadButton: {
    flex: 2,
    backgroundColor: '#007AFF',
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  uploadButtonDisabled: {
    opacity: 0.5,
  },
  uploadButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});

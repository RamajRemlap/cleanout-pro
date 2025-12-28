/**
 * Room List Screen
 * Shows all rooms for a job + add new room
 */

import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  FlatList,
  TouchableOpacity,
  StyleSheet,
  RefreshControl,
  ActivityIndicator,
  Image,
} from 'react-native';
import { useAppStore } from '../store';
import apiService from '../services/api';
import { Room } from '../types';

interface Props {
  navigation: any;
  route: any;
}

export const RoomListScreen: React.FC<Props> = ({ navigation, route }) => {
  const { jobId } = route.params;
  const [refreshing, setRefreshing] = useState(false);
  const [loading, setLoading] = useState(true);
  const { currentJob, rooms, setRooms } = useAppStore();

  useEffect(() => {
    loadRooms();
  }, [jobId]);

  const loadRooms = async () => {
    try {
      setLoading(true);
      const data = await apiService.getRooms(jobId);
      setRooms(data);
    } catch (error) {
      console.error('Failed to load rooms:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    await loadRooms();
    setRefreshing(false);
  };

  const handleAddRoom = () => {
    navigation.navigate('Capture', {
      jobId,
      roomNumber: rooms.length + 1,
    });
  };

  const handleRoomPress = (room: Room) => {
    navigation.navigate('RoomDetail', { room });
  };

  const renderRoom = ({ item }: { item: Room }) => {
    const sizeLabel = {
      small: 'S',
      medium: 'M',
      large: 'L',
      extra_large: 'XL',
    }[item.final_size_class];

    const workloadLabel = {
      light: 'Light',
      moderate: 'Moderate',
      heavy: 'Heavy',
      extreme: 'Extreme',
    }[item.final_workload_class];

    const confidenceColor =
      item.ai_confidence && item.ai_confidence >= 0.7
        ? '#34C759'
        : item.ai_confidence && item.ai_confidence >= 0.5
        ? '#FF9500'
        : '#FF3B30';

    return (
      <TouchableOpacity
        style={styles.roomCard}
        onPress={() => handleRoomPress(item)}>
        {item.image_url && (
          <Image
            source={{ uri: item.image_url }}
            style={styles.roomImage}
            resizeMode="cover"
          />
        )}

        <View style={styles.roomContent}>
          <View style={styles.roomHeader}>
            <Text style={styles.roomName}>{item.name}</Text>
            <View style={styles.badges}>
              <View style={styles.sizeBadge}>
                <Text style={styles.badgeText}>{sizeLabel}</Text>
              </View>
            </View>
          </View>

          <Text style={styles.workloadText}>{workloadLabel} workload</Text>

          {item.ai_confidence !== undefined && (
            <View style={styles.confidenceRow}>
              <Text style={styles.confidenceLabel}>AI Confidence:</Text>
              <Text style={[styles.confidenceValue, { color: confidenceColor }]}>
                {(item.ai_confidence * 100).toFixed(0)}%
              </Text>
            </View>
          )}

          {item.human_size_class && (
            <Text style={styles.overrideText}>
              ✓ Human verified
            </Text>
          )}

          <View style={styles.priceRow}>
            <Text style={styles.priceLabel}>Estimate:</Text>
            <Text style={styles.priceValue}>
              ${item.estimated_cost.toFixed(2)}
            </Text>
          </View>
        </View>
      </TouchableOpacity>
    );
  };

  if (loading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#007AFF" />
        <Text style={styles.loadingText}>Loading rooms...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>
          Job #{currentJob?.job_number || 'Unknown'}
        </Text>
        <Text style={styles.headerSubtitle}>
          {rooms.length} {rooms.length === 1 ? 'room' : 'rooms'}
        </Text>
      </View>

      <FlatList
        data={rooms}
        renderItem={renderRoom}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.listContent}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={handleRefresh} />
        }
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Text style={styles.emptyText}>No rooms captured yet</Text>
            <Text style={styles.emptySubtext}>
              Tap the camera button to add a room
            </Text>
          </View>
        }
      />

      <TouchableOpacity style={styles.addButton} onPress={handleAddRoom}>
        <Text style={styles.addButtonText}>📷 Add Room</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F5F5F5',
  },
  header: {
    backgroundColor: '#fff',
    paddingHorizontal: 20,
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#E5E5E5',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#666',
    marginTop: 4,
  },
  listContent: {
    padding: 16,
    paddingBottom: 100,
  },
  roomCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
    overflow: 'hidden',
  },
  roomImage: {
    width: '100%',
    height: 200,
  },
  roomContent: {
    padding: 16,
  },
  roomHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  roomName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    flex: 1,
  },
  badges: {
    flexDirection: 'row',
  },
  sizeBadge: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 12,
  },
  badgeText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '600',
  },
  workloadText: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
  },
  confidenceRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  confidenceLabel: {
    fontSize: 14,
    color: '#666',
    marginRight: 8,
  },
  confidenceValue: {
    fontSize: 14,
    fontWeight: '600',
  },
  overrideText: {
    fontSize: 14,
    color: '#34C759',
    fontWeight: '600',
    marginBottom: 8,
  },
  priceRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 8,
    paddingTop: 8,
    borderTopWidth: 1,
    borderTopColor: '#E5E5E5',
  },
  priceLabel: {
    fontSize: 14,
    color: '#666',
  },
  priceValue: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#34C759',
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: '#666',
  },
  emptyContainer: {
    alignItems: 'center',
    marginTop: 60,
  },
  emptyText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#666',
  },
  emptySubtext: {
    fontSize: 14,
    color: '#999',
    marginTop: 8,
  },
  addButton: {
    position: 'absolute',
    bottom: 20,
    left: 20,
    right: 20,
    backgroundColor: '#007AFF',
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 8,
    elevation: 5,
  },
  addButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});

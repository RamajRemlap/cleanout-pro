/**
 * Room Detail Screen
 * Shows full AI classification details and reasoning
 */

import React from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  Image,
  TouchableOpacity,
} from 'react-native';
import { Room } from '../types';

interface Props {
  navigation: any;
  route: any;
}

export const RoomDetailScreen: React.FC<Props> = ({ navigation, route }) => {
  const { room } = route.params as { room: Room };

  const sizeLabels = {
    small: 'Small',
    medium: 'Medium',
    large: 'Large',
    extra_large: 'Extra Large',
  };

  const workloadLabels = {
    light: 'Light',
    moderate: 'Moderate',
    heavy: 'Heavy',
    extreme: 'Extreme',
  };

  return (
    <ScrollView style={styles.container}>
      {room.image_url && (
        <Image
          source={{ uri: room.image_url }}
          style={styles.image}
          resizeMode="cover"
        />
      )}

      <View style={styles.content}>
        <Text style={styles.roomName}>{room.name}</Text>
        <Text style={styles.roomNumber}>Room #{room.room_number}</Text>

        {/* Estimate */}
        <View style={styles.estimateCard}>
          <Text style={styles.estimateLabel}>Estimated Cost</Text>
          <Text style={styles.estimateValue}>
            ${room.estimated_cost.toFixed(2)}
          </Text>
        </View>

        {/* Final Classification */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Final Classification</Text>
          <View style={styles.classificationRow}>
            <View style={styles.classificationItem}>
              <Text style={styles.classificationLabel}>Size</Text>
              <Text style={styles.classificationValue}>
                {sizeLabels[room.final_size_class]}
              </Text>
            </View>
            <View style={styles.classificationItem}>
              <Text style={styles.classificationLabel}>Workload</Text>
              <Text style={styles.classificationValue}>
                {workloadLabels[room.final_workload_class]}
              </Text>
            </View>
          </View>
        </View>

        {/* AI Analysis */}
        {room.ai_size_class && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>AI Analysis</Text>

            <View style={styles.aiRow}>
              <Text style={styles.aiLabel}>Size Class:</Text>
              <Text style={styles.aiValue}>
                {sizeLabels[room.ai_size_class]}
              </Text>
            </View>

            <View style={styles.aiRow}>
              <Text style={styles.aiLabel}>Workload Class:</Text>
              <Text style={styles.aiValue}>
                {workloadLabels[room.ai_workload_class!]}
              </Text>
            </View>

            {room.ai_confidence !== undefined && (
              <View style={styles.aiRow}>
                <Text style={styles.aiLabel}>Confidence:</Text>
                <Text
                  style={[
                    styles.aiValue,
                    {
                      color:
                        room.ai_confidence >= 0.7
                          ? '#34C759'
                          : room.ai_confidence >= 0.5
                          ? '#FF9500'
                          : '#FF3B30',
                    },
                  ]}>
                  {(room.ai_confidence * 100).toFixed(0)}%
                </Text>
              </View>
            )}

            {room.ai_reasoning && (
              <View style={styles.reasoningBox}>
                <Text style={styles.reasoningLabel}>AI Reasoning:</Text>
                <Text style={styles.reasoningText}>{room.ai_reasoning}</Text>
              </View>
            )}
          </View>
        )}

        {/* Human Override */}
        {room.human_size_class && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Human Verification ✓</Text>

            <View style={styles.aiRow}>
              <Text style={styles.aiLabel}>Adjusted Size:</Text>
              <Text style={styles.aiValue}>
                {sizeLabels[room.human_size_class]}
              </Text>
            </View>

            {room.human_workload_class && (
              <View style={styles.aiRow}>
                <Text style={styles.aiLabel}>Adjusted Workload:</Text>
                <Text style={styles.aiValue}>
                  {workloadLabels[room.human_workload_class]}
                </Text>
              </View>
            )}

            {room.human_override_reason && (
              <View style={styles.reasoningBox}>
                <Text style={styles.reasoningLabel}>Reason:</Text>
                <Text style={styles.reasoningText}>
                  {room.human_override_reason}
                </Text>
              </View>
            )}
          </View>
        )}

        {/* Metadata */}
        <View style={styles.metadata}>
          <Text style={styles.metadataText}>
            Captured: {new Date(room.captured_at).toLocaleString()}
          </Text>
          {room.processed_at && (
            <Text style={styles.metadataText}>
              Processed: {new Date(room.processed_at).toLocaleString()}
            </Text>
          )}
        </View>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  image: {
    width: '100%',
    height: 300,
  },
  content: {
    padding: 20,
  },
  roomName: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#333',
  },
  roomNumber: {
    fontSize: 16,
    color: '#666',
    marginTop: 4,
    marginBottom: 20,
  },
  estimateCard: {
    backgroundColor: '#34C759',
    borderRadius: 12,
    padding: 20,
    alignItems: 'center',
    marginBottom: 20,
  },
  estimateLabel: {
    fontSize: 16,
    color: 'rgba(255, 255, 255, 0.9)',
    marginBottom: 4,
  },
  estimateValue: {
    fontSize: 36,
    fontWeight: 'bold',
    color: '#fff',
  },
  section: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 12,
  },
  classificationRow: {
    flexDirection: 'row',
    gap: 16,
  },
  classificationItem: {
    flex: 1,
    backgroundColor: '#F5F5F5',
    padding: 12,
    borderRadius: 8,
  },
  classificationLabel: {
    fontSize: 14,
    color: '#666',
    marginBottom: 4,
  },
  classificationValue: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#007AFF',
  },
  aiRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#F5F5F5',
  },
  aiLabel: {
    fontSize: 16,
    color: '#666',
  },
  aiValue: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  reasoningBox: {
    backgroundColor: '#F5F5F5',
    padding: 12,
    borderRadius: 8,
    marginTop: 12,
  },
  reasoningLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: '#666',
    marginBottom: 8,
  },
  reasoningText: {
    fontSize: 14,
    color: '#333',
    lineHeight: 20,
  },
  metadata: {
    marginTop: 20,
    paddingTop: 20,
    borderTopWidth: 1,
    borderTopColor: '#E5E5E5',
  },
  metadataText: {
    fontSize: 14,
    color: '#999',
    marginBottom: 4,
  },
});

/**
 * Job List Screen
 * Shows all jobs for field workers
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
} from 'react-native';
import { useAppStore } from '../store';
import apiService from '../services/api';
import syncService from '../services/sync';
import { Job } from '../types';

interface Props {
  navigation: any;
}

export const JobListScreen: React.FC<Props> = ({ navigation }) => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [refreshing, setRefreshing] = useState(false);
  const [loading, setLoading] = useState(true);
  const { setCurrentJob, isOffline, pendingSyncCount } = useAppStore();

  useEffect(() => {
    loadJobs();
  }, []);

  const loadJobs = async () => {
    try {
      setLoading(true);
      const data = await apiService.getJobs();
      setJobs(data);
    } catch (error) {
      console.error('Failed to load jobs:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    await loadJobs();

    // Sync pending operations
    const result = await syncService.processQueue();
    if (result.success > 0) {
      console.log(`Synced ${result.success} operations`);
    }

    setRefreshing(false);
  };

  const handleSelectJob = (job: Job) => {
    setCurrentJob(job);
    navigation.navigate('RoomList', { jobId: job.id });
  };

  const renderJob = ({ item }: { item: Job }) => {
    const statusColor = {
      scheduled: '#007AFF',
      in_progress: '#FF9500',
      completed: '#34C759',
      cancelled: '#FF3B30',
    }[item.status];

    return (
      <TouchableOpacity
        style={styles.jobCard}
        onPress={() => handleSelectJob(item)}>
        <View style={styles.jobHeader}>
          <Text style={styles.jobNumber}>#{item.job_number}</Text>
          <View style={[styles.statusBadge, { backgroundColor: statusColor }]}>
            <Text style={styles.statusText}>
              {item.status.replace('_', ' ').toUpperCase()}
            </Text>
          </View>
        </View>

        <Text style={styles.customerName}>
          {item.customer?.name || 'Unknown Customer'}
        </Text>

        {item.customer?.address && (
          <Text style={styles.address}>{item.customer.address}</Text>
        )}

        {item.scheduled_date && (
          <Text style={styles.scheduledDate}>
            Scheduled: {new Date(item.scheduled_date).toLocaleDateString()}
          </Text>
        )}

        <View style={styles.priceRow}>
          <Text style={styles.priceLabel}>Estimate:</Text>
          <Text style={styles.priceValue}>
            ${item.ai_estimate?.toFixed(2) || '0.00'}
          </Text>
        </View>
      </TouchableOpacity>
    );
  };

  if (loading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#007AFF" />
        <Text style={styles.loadingText}>Loading jobs...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Header with sync status */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>My Jobs</Text>
        {isOffline && (
          <View style={styles.offlineBadge}>
            <Text style={styles.offlineText}>Offline</Text>
          </View>
        )}
        {pendingSyncCount > 0 && (
          <View style={styles.syncBadge}>
            <Text style={styles.syncText}>{pendingSyncCount} pending</Text>
          </View>
        )}
      </View>

      <FlatList
        data={jobs}
        renderItem={renderJob}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.listContent}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={handleRefresh} />
        }
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Text style={styles.emptyText}>No jobs found</Text>
            <Text style={styles.emptySubtext}>
              Pull down to refresh
            </Text>
          </View>
        }
      />
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
    flexDirection: 'row',
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    flex: 1,
  },
  offlineBadge: {
    backgroundColor: '#FF9500',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
    marginLeft: 8,
  },
  offlineText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '600',
  },
  syncBadge: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
    marginLeft: 8,
  },
  syncText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '600',
  },
  listContent: {
    padding: 16,
  },
  jobCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  jobHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  jobNumber: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  statusBadge: {
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 12,
  },
  statusText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '600',
  },
  customerName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 4,
  },
  address: {
    fontSize: 14,
    color: '#666',
    marginBottom: 4,
  },
  scheduledDate: {
    fontSize: 14,
    color: '#666',
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
});

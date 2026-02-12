import { useState, useEffect, useCallback } from 'react';
import { fetchContentBlocks, fetchSubjectIndicators, fetchObjectIndicators, fetchRelationsContentBlocks } from '../services/api';
import { CONTENT_BLOCKS } from '../constants/contentBlocks';
import { SUBJECT_INDICATORS, OBJECT_INDICATORS, RELATIONS_CONTENT } from '../constants/relationsConfig';

export const useContentData = () => {
  const [contentBlocks, setContentBlocks] = useState(CONTENT_BLOCKS);
  const [subjectIndicators, setSubjectIndicators] = useState(SUBJECT_INDICATORS);
  const [objectIndicators, setObjectIndicators] = useState(OBJECT_INDICATORS);
  const [relationsContentBlocks, setRelationsContentBlocks] = useState(RELATIONS_CONTENT);
  const [loading, setLoading] = useState(true);
  const [isError, setIsError] = useState(false);

  const loadData = useCallback(async () => {
    setLoading(true);
    setIsError(false);
    try {
      const [contentData, subjectData, objectData, relationsData] = await Promise.all([
        fetchContentBlocks(),
        fetchSubjectIndicators(),
        fetchObjectIndicators(),
        fetchRelationsContentBlocks()
      ]);

      // Use data from server or fallback to constants
      if (contentData) setContentBlocks(contentData);
      if (subjectData) setSubjectIndicators(subjectData);
      if (objectData) setObjectIndicators(objectData);
      if (relationsData) setRelationsContentBlocks(relationsData);
      
      // If all requests failed, mark as error
      if (!contentData && !subjectData && !objectData && !relationsData) {
        setIsError(true);
        console.warn('All API requests failed, using fallback data from constants');
      }
    } catch (err) {
      setIsError(true);
      console.error('Error loading data:', err);
      console.warn('Using fallback data from constants');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  return {
    contentBlocks,
    subjectIndicators,
    objectIndicators,
    relationsContentBlocks,
    loading,
    isError,
    refetch: loadData
  };
};

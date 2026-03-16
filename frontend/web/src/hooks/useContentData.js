import { useState, useEffect, useCallback } from 'react';
import { fetchContentBlocks, fetchSubjectIndicators, fetchObjectIndicators, fetchRelationsContentBlocks } from '../services/api';
import { CONTENT_BLOCKS } from '../constants/contentBlocks';
import { SUBJECT_INDICATORS, OBJECT_INDICATORS, RELATIONS_CONTENT } from '../constants/relationsConfig';

export const useContentData = () => {
  const [contentBlocks, setContentBlocks] = useState({});
  const [subjectIndicators, setSubjectIndicators] = useState([]);
  const [objectIndicators, setObjectIndicators] = useState([]);
  const [relationsContentBlocks, setRelationsContentBlocks] = useState({});
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

      const hasContentData = contentData && Object.keys(contentData).length > 0;
      const hasSubjectData = Array.isArray(subjectData) && subjectData.length > 0;
      const hasObjectData = Array.isArray(objectData) && objectData.length > 0;
      const hasRelationsData = relationsData && Object.keys(relationsData).length > 0;

      // Prefer DB/API data and only fallback when it is missing
      setContentBlocks(hasContentData ? contentData : CONTENT_BLOCKS);
      setSubjectIndicators(hasSubjectData ? subjectData : SUBJECT_INDICATORS);
      setObjectIndicators(hasObjectData ? objectData : OBJECT_INDICATORS);
      setRelationsContentBlocks(hasRelationsData ? relationsData : RELATIONS_CONTENT);
      
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

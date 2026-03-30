import { useState, useEffect, useCallback, useContext, useMemo } from 'react';
import { RegionContext } from '../context/RegionContext';
import { getRegionConfig } from '../data/regions';
import { fetchContentBlocks, fetchSubjectIndicators, fetchObjectIndicators, fetchRelationsContentBlocks } from '../services/api';

export const useContentData = () => {
  //const [contentBlocks, setContentBlocks] = useState({});
  //const [subjectIndicators, setSubjectIndicators] = useState([]);
  //const [objectIndicators, setObjectIndicators] = useState([]);
  //const [relationsContentBlocks, setRelationsContentBlocks] = useState({});
  const { region } = useContext(RegionContext);

  const regionConfig = useMemo(() => getRegionConfig(region), [region]);

  const [contentBlocks, setContentBlocks] = useState(regionConfig.contentBlocks);
  const [subjectIndicators, setSubjectIndicators] = useState(regionConfig.subjectIndicators);
  const [objectIndicators, setObjectIndicators] = useState(regionConfig.objectIndicators);
  const [relationsContentBlocks, setRelationsContentBlocks] = useState(regionConfig.relationsContent);
  const [loading, setLoading] = useState(true);
  const [isError, setIsError] = useState(false);

  useEffect(() => {
    setContentBlocks(regionConfig.contentBlocks);
    setSubjectIndicators(regionConfig.subjectIndicators);
    setObjectIndicators(regionConfig.objectIndicators);
    setRelationsContentBlocks(regionConfig.relationsContent);
  }, [regionConfig]);

  const loadData = useCallback(async () => {
    if (!regionConfig.hasData) {
      setLoading(false);
      return;
    }

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
      setContentBlocks(hasContentData ? contentData : regionConfig.contentBlocks);
      setSubjectIndicators(hasSubjectData ? subjectData : regionConfig.subjectIndicators);
      setObjectIndicators(hasObjectData ? objectData : regionConfig.objectIndicators);
      setRelationsContentBlocks(hasRelationsData ? relationsData : regionConfig.relationsContent);

      if (!contentData && !subjectData && !objectData && !relationsData) {
        setIsError(true);
        console.warn('All API requests failed, using fallback data from region config');
      }
    } catch (err) {
      setIsError(true);
      console.error('Error loading data:', err);
      console.warn('Using fallback data from region config');
    } finally {
      setLoading(false);
    }
  }, [regionConfig]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  return {
    contentBlocks,
    subjectIndicators,
    objectIndicators,
    relationsContentBlocks,
    hasData: regionConfig.hasData,
    geojsonPath: regionConfig.geojsonPath,
    loading,
    isError,
    refetch: loadData
  };
};

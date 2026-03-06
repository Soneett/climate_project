import { CONTENT_BLOCKS as altaiContent } from './altaiRepublic/contentBlocks';
import {
  RELATIONS_CONTENT as altaiRelations,
  SUBJECT_INDICATORS as altaiSubjects,
  OBJECT_INDICATORS as altaiObjects,
} from './altaiRepublic/relationsContent';

export const REGIONS_CONFIG = {
  'Республика Алтай': {
    id: 'altai-republic',
    name: 'Республика Алтай',
    contentBlocks: altaiContent,
    relationsContent: altaiRelations,
    subjectIndicators: altaiSubjects,
    objectIndicators: altaiObjects,
    geojsonPath: '/altai.geojson',
    hasData: true,
  },
  'Алтайский край': {
    id: 'altai-krai',
    name: 'Алтайский край',
    contentBlocks: altaiContent,
    relationsContent: altaiRelations,
    subjectIndicators: altaiSubjects,
    objectIndicators: altaiObjects,
    geojsonPath: '/altai.geojson',
    hasData: true,
  },
  'Свердловская область': {
    id: 'sverdlovsk',
    name: 'Свердловская область',
    contentBlocks: {},
    relationsContent: {},
    subjectIndicators: [],
    objectIndicators: [],
    geojsonPath: null,
    hasData: false,
  },
};

export const getRegionConfig = (regionName) => {
  return (
    REGIONS_CONFIG[regionName] || {
      id: 'unknown',
      name: regionName,
      contentBlocks: {},
      relationsContent: {},
      subjectIndicators: [],
      objectIndicators: [],
      hasData: false,
    }
  );
};
